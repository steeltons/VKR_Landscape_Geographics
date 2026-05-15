import logging

from app.ml.artifacts.model_artifact_storage import ModelArtifactStorage
from app.ml.models.base_model import BaseModel
from app.ml.models.catboost_model import CatBoostModel


logger = logging.getLogger(__name__)


class ModelRegistry:
    def __init__(self) -> None:
        self.artifact_storage = ModelArtifactStorage()
        self._models: dict[str, BaseModel] = {}

    def get_model(self, name: str = "default") -> BaseModel:
        if name not in self._models:
            if name == "default":
                version = self.artifact_storage.get_current_model_version()
                self._models[name] = CatBoostModel(version=version, artifact_storage=self.artifact_storage)
            else:
                raise ValueError(f"Unknown model: {name}")

        return self._models[name]

    def preload_current_model(self) -> None:
        logger.info("START ModelRegistry::preload_current_model")

        version = self.artifact_storage.get_current_model_version()
        model = CatBoostModel(version=version, artifact_storage=self.artifact_storage)
        model.load()

        self._models["default"] = model

        logger.info("END ModelRegistry::preload_current_model version=%s", version)

    def activate_model_version(self, *, version: str) -> None:
        logger.info("START ModelRegistry::activate_model_version version=%s", version)

        self.artifact_storage.set_current_model_version(version=version)

        model = CatBoostModel(version=version, artifact_storage=self.artifact_storage)
        model.load()

        self._models["default"] = model

        logger.info("END ModelRegistry::activate_model_version version=%s", version)


model_registry = ModelRegistry()


def get_model_registry() -> ModelRegistry:
    return model_registry