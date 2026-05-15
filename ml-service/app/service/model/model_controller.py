import logging

from fastapi import APIRouter, HTTPException, status

from app.service.model.model_dto import ModelMetadataRsDto, ModelTrainRqDto, ModelTrainRsDto
from app.service.model.model_service import ModelService


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/models", tags=["models"])


@router.post("", response_model=ModelTrainRsDto, status_code=status.HTTP_201_CREATED)
async def train_model(request: ModelTrainRqDto) -> ModelTrainRsDto:
    params = request.model_dump()
    logger.info("START ModelController::train_model %s", params)

    service = ModelService()

    try:
        result = await service.train_model(request)
    except Exception as exc:
        logger.exception("END ModelController::train_model %s error=%s", params, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model training failed: {str(exc)}",
        ) from exc

    logger.info("END ModelController::train_model %s %s", params, result)

    return result


@router.get("/actual", response_model=ModelMetadataRsDto)
async def get_actual_model_metadata() -> ModelMetadataRsDto:
    logger.debug("START ModelController::get_actual_model_metadata")

    service = ModelService()
    result = await service.get_actual_model_metadata()

    logger.debug("END ModelController::get_actual_model_metadata %s", result)

    return result


@router.get("", response_model=list[ModelMetadataRsDto])
async def get_all_model_metadata() -> list[ModelMetadataRsDto]:
    logger.debug("START ModelController::get_all_model_metadata")

    service = ModelService()
    result = await service.get_all_model_metadata()

    logger.debug("END ModelController::get_all_model_metadata count=%s", len(result))

    return result

@router.post("/activation/{model_version}", response_model=ModelMetadataRsDto)
async def activate_model_version(model_version: str) -> ModelMetadataRsDto:
    params = {"model_version": model_version}
    logger.info("START ModelController::activate_model_version %s", params)

    service = ModelService()

    try:
        result = await service.activate_model_version(model_version)
    except FileNotFoundError as exc:
        logger.warning("END ModelController::activate_model_version %s not_found=%s", params, str(exc))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("END ModelController::activate_model_version %s error=%s", params, str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model activation failed: {str(exc)}",
        ) from exc

    logger.info("END ModelController::activate_model_version %s %s", params, result)

    return result

@router.get("/{model_version}", response_model=ModelMetadataRsDto)
async def get_model_metadata(model_version: str) -> ModelMetadataRsDto:
    params = {"model_version": model_version}
    logger.debug("START ModelController::get_model_metadata %s", params)

    service = ModelService()
    result = await service.get_model_metadata(model_version)

    logger.debug("END ModelController::get_model_metadata %s %s", params, result)

    return result
