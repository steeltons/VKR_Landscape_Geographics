import logging

from starlette.concurrency import run_in_threadpool

from app.configs.config import settings
from app.ml.artifacts.model_artifact_storage import ModelArtifactStorage
from app.ml.models.model_registry import get_model_registry
from app.ml.training.model_trainer import train_model
from app.service.model.model_dto import ModelMetadataRsDto, ModelTrainRqDto, ModelTrainRsDto


logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self) -> None:
        self.model_registry = get_model_registry()
        self.artifact_storage = ModelArtifactStorage()

    async def train_model(self, request: ModelTrainRqDto) -> ModelTrainRsDto:
        params = request.model_dump()

        logger.info("START ModelService::train_model %s", params)

        metrics = await run_in_threadpool(train_model, version=request.version)

        if request.reload_after_train:
            await run_in_threadpool(self.model_registry.activate_model_version, version=request.version)

        result = ModelTrainRsDto(
            version=request.version,
            model_object_name=settings.build_model_object_name(request.version),
            metrics_object_name=settings.build_metrics_object_name(request.version),
            dataset_object_name=settings.build_dataset_object_name(request.version),
            metrics=metrics,
        )

        logger.info("END ModelService::train_model %s %s", params, result)

        return result

    async def get_actual_model_metadata(self) -> ModelMetadataRsDto:
        logger.debug("START ModelService::get_actual_model_metadata")

        metadata = await run_in_threadpool(self.artifact_storage.get_actual_model_metadata)
        result = ModelMetadataRsDto(**metadata)

        logger.debug("END ModelService::get_actual_model_metadata %s", result)

        return result

    async def get_all_model_metadata(self) -> list[ModelMetadataRsDto]:
        logger.debug("START ModelService::get_all_model_metadata")

        items = await run_in_threadpool(self.artifact_storage.list_model_metadata)
        result = [ModelMetadataRsDto(**item) for item in items]

        logger.debug("END ModelService::get_all_model_metadata count=%s", len(result))

        return result

    async def get_model_metadata(self, version: str) -> ModelMetadataRsDto:
        logger.debug("START ModelService::get_model_metadata version=%s", version)

        metadata = await run_in_threadpool(self.artifact_storage.get_model_metadata, version=version)
        result = ModelMetadataRsDto(**metadata)

        logger.debug("END ModelService::get_model_metadata version=%s result=%s", version, result)

        return result

    async def activate_model_version(self, version: str) -> ModelMetadataRsDto:
        logger.info("START ModelService::activate_model_version version=%s", version)

        metadata = await run_in_threadpool(self.artifact_storage.get_model_metadata, version=version)

        if not metadata.get("model_exists"):
            raise FileNotFoundError(f"Model version not found: {version}")

        await run_in_threadpool(self.model_registry.activate_model_version, version=version)

        metadata = await run_in_threadpool(self.artifact_storage.get_model_metadata, version=version)
        result = ModelMetadataRsDto(**metadata)

        logger.info("END ModelService::activate_model_version version=%s result=%s", version, result)

        return result