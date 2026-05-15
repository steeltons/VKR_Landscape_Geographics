import logging

import numpy as np
from catboost import CatBoostRegressor

from app.configs.config import settings
from app.ml.artifacts.model_artifact_storage import ModelArtifactStorage
from app.ml.features.feature_schema import FEATURES
from app.ml.models.base_model import BaseModel


logger = logging.getLogger(__name__)


class CatBoostModel(BaseModel):

    def __init__(self, *, version: str | None = None, artifact_storage: ModelArtifactStorage | None = None) -> None:
        self.version = version or settings.model_current_version
        self.artifact_storage = artifact_storage or ModelArtifactStorage()

        self.model = CatBoostRegressor()
        self._is_loaded = False

    def load(self) -> None:
        if self._is_loaded:
            return

        logger.info("START CatBoostModel::load version=%s", self.version)

        model_path = self.artifact_storage.download_model_to_local_file(version=self.version)

        self.model.load_model(str(model_path))
        self._is_loaded = True

        logger.info("END CatBoostModel::load version=%s model_path=%s", self.version, model_path)

    def reload(self, *, version: str | None = None) -> None:
        if version is not None:
            self.version = version

        self.model = CatBoostRegressor()
        self._is_loaded = False
        self.load()

    def _prepare_features(self, features: dict[str, float | int]) -> np.ndarray:
        return np.array([[features.get(name, 0.0) for name in FEATURES]])

    def predict(self, features: dict[str, float | int]) -> float:
        self.load()

        x = self._prepare_features(features)
        score = float(self.model.predict(x)[0])

        return max(0.0, min(score, 1.0))

    def predict_proba(self, features: dict[str, float | int]) -> float:
        return self.predict(features)