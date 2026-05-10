from pathlib import Path

import numpy as np
from catboost import CatBoostRegressor

from app.configs.config import settings
from app.ml.features.feature_schema import FEATURES
from app.ml.models.base_model import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class CatBoostModel(BaseModel):
    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or settings.default_model_name

        artifacts_dir = Path(settings.model_artifacts_dir)

        if not artifacts_dir.is_absolute():
            artifacts_dir = PROJECT_ROOT / artifacts_dir

        self.model_path = artifacts_dir / f"{self.model_name}.cbm"

        self.model = CatBoostRegressor()
        self._is_loaded = False

    def load(self) -> None:
        if self._is_loaded:
            return

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        self.model.load_model(str(self.model_path))
        self._is_loaded = True

    def _prepare_features(self, features: dict[str, float | int]) -> np.ndarray:
        return np.array([
            [features.get(name, 0.0) for name in FEATURES]
        ])

    def predict(self, features: dict[str, float | int]) -> float:
        self.load()

        x = self._prepare_features(features)
        score = float(self.model.predict(x)[0])

        return max(0.0, min(score, 1.0))

    def predict_proba(self, features: dict[str, float | int]) -> float:
        return self.predict(features)