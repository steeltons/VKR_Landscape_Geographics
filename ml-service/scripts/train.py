import json
import sys
from pathlib import Path

from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from app.configs.config import settings
from app.ml.features.feature_schema import FEATURES
from app.ml.training.dataset_builder import DatasetBuilder
from app.ml.training.weak_labeler import WeakLabeler


def main() -> None:
    artifacts_dir = Path(settings.model_artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    dataset_builder = DatasetBuilder()
    labeler = WeakLabeler()

    df = dataset_builder.build()
    df = labeler.build_labels(df)

    if df.empty:
        raise RuntimeError("Training dataset is empty")

    dataset_path = artifacts_dir / "training_dataset.csv"
    df.to_csv(dataset_path, index=False)

    X = df[FEATURES]
    y = df["target_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = CatBoostRegressor(
        iterations=700,
        depth=5,
        learning_rate=0.04,
        loss_function="RMSE",
        eval_metric="RMSE",
        random_seed=42,
        verbose=50,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=(X_test, y_test),
        use_best_model=True,
        early_stopping_rounds=100,
    )

    predictions = model.predict(X_test)

    feature_importances = model.get_feature_importance()

    metrics = {
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
            {
                "feature": feature,
                "importance": float(importance),
            }
            for feature, importance in zip(FEATURES, feature_importances)
        ],
        "features": FEATURES,
    }

    model_path = artifacts_dir / f"{settings.default_model_name}.cbm"
    metrics_path = artifacts_dir / "training_metrics.json"

    model.save_model(model_path)

    with open(metrics_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=2)

    print(f"Dataset saved: {dataset_path}")
    print(f"Model saved: {model_path}")
    print(f"Metrics saved: {metrics_path}")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()