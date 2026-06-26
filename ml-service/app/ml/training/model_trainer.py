import json
from pathlib import Path
from typing import Any

from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.configs.config import settings
from app.ml.artifacts.model_artifact_storage import ModelArtifactStorage
from app.ml.features.feature_schema import FEATURES
from app.ml.training.dataset_builder import DatasetBuilder
from app.ml.training.weak_labeler import WeakLabeler


def train_model(*, version: str) -> dict[str, Any]:
    normalized_version = settings._normalize_version(version)

    local_artifacts_dir = Path(settings.model_local_tmp_dir) / "training" / normalized_version
    local_artifacts_dir.mkdir(parents=True, exist_ok=True)

    catboost_train_dir = Path(settings.catboost_train_dir) / normalized_version
    catboost_train_dir.mkdir(parents=True, exist_ok=True)

    dataset_builder = DatasetBuilder()
    labeler = WeakLabeler()

    df = dataset_builder.build()
    df = labeler.build_labels(df)

    if df.empty:
        raise RuntimeError("Training dataset is empty")

    dataset_path = local_artifacts_dir / settings.model_dataset_filename
    df.to_csv(dataset_path, index=False)

    X = df[FEATURES]
    y = df["target_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = CatBoostRegressor(
        iterations=700,
        depth=5,
        learning_rate=0.04,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=42,
        verbose=50,
        train_dir=str(catboost_train_dir),
    )

    model.fit(X_train, y_train, eval_set=(X_test, y_test), use_best_model=True, early_stopping_rounds=100)

    predictions = model.predict(X_test)
    feature_importances = model.get_feature_importance()

    metrics = {
        "version": version,
        "dataset_size": int(len(df)),
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "target_score_min": float(df["target_score"].min()),
        "target_score_max": float(df["target_score"].max()),
        "target_score_mean": float(df["target_score"].mean()),
        "mae": float(mean_absolute_error(y_test, predictions)),
        "mse": float(mean_squared_error(y_test, predictions)),
        "rmse": float(mean_squared_error(y_test, predictions) ** 0.5),
        "r2": float(r2_score(y_test, predictions)),
        "label_distribution": {
            str(key): int(value)
            for key, value in df["target_label"].value_counts().to_dict().items()
        },
        "feature_importance": [
            {"feature": feature, "importance": float(importance)}
            for feature, importance in zip(FEATURES, feature_importances)
        ],
        "features": FEATURES,
        "minio": {
            "model_object_name": settings.build_model_object_name(version),
            "metrics_object_name": settings.build_metrics_object_name(version),
            "dataset_object_name": settings.build_dataset_object_name(version),
        },
    }

    model_path = local_artifacts_dir / settings.model_filename
    metrics_path = local_artifacts_dir / settings.model_metrics_filename

    model.save_model(model_path)

    with metrics_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=2)

    artifact_storage = ModelArtifactStorage()
    artifact_storage.upload_model_artifacts(
        version=version,
        model_path=model_path,
        metrics_path=metrics_path,
        dataset_path=dataset_path,
    )

    return metrics