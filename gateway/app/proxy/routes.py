import logging
import uuid
from io import BytesIO
from urllib.parse import quote

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from starlette import status

from app.configs.config import settings
from app.proxy.client import ProxyClient
from app.service.file_metadata_dto import FileDownloadData, FileUploadRsDto
from app.service.file_metadata_service import FileMetadataService
from app.service.territory_recommendation_dto import (
    TerritoryPointSearchWithRecommendationRsDto,
)
from app.service.territory_service import TerritoryService


logger = logging.getLogger(__name__)

router = APIRouter()

proxy_client = ProxyClient(
    timeout_seconds=settings.request_timeout_seconds,
)


def build_file_response(file_data: FileDownloadData) -> StreamingResponse:
    filename = quote(file_data.filename)

    return StreamingResponse(
        BytesIO(file_data.content),
        media_type=file_data.media_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{filename}",
            "Content-Length": str(len(file_data.content)),
        },
    )


@router.post(
    "/user-microservice/api/v1/files",
    response_model=FileUploadRsDto,
)
async def proxy_upload_user_file(
    file_group: str = Query(..., description="Группа файла"),
    file: UploadFile = File(...),
) -> FileUploadRsDto:
    params_for_log = {
        "file_group": file_group,
        "filename": file.filename,
        "content_type": file.content_type,
    }

    logger.info(
        "START GatewayFileController::proxy_upload_user_file %s",
        params_for_log,
    )

    if not file_group.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Параметр file_group обязателен.",
        )

    service = FileMetadataService()

    result = await service.save_user_microservice_file(
        file=file,
        file_group=file_group.strip(),
    )

    logger.info(
        "END GatewayFileController::proxy_upload_user_file %s %s",
        params_for_log,
        result,
    )

    return result


@router.get(
    "/user-microservice/api/v1/files/{file_id}",
)
async def proxy_download_user_file(
    file_id: uuid.UUID,
) -> StreamingResponse:
    params_for_log = {
        "file_id": file_id,
    }

    logger.debug(
        "START GatewayFileController::proxy_download_user_file %s",
        params_for_log,
    )

    service = FileMetadataService()

    result = await service.download_user_microservice_file(
        file_id=file_id,
    )

    if result is None:
        logger.debug(
            "END GatewayFileController::proxy_download_user_file %s None",
            params_for_log,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден.",
        )

    logger.debug(
        "END GatewayFileController::proxy_download_user_file %s filename=%s",
        params_for_log,
        result.filename,
    )

    return build_file_response(result)


@router.api_route(
    "/user-microservice/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def proxy_users(
    path: str,
    request: Request,
):
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.users_service_url,
        path="/" + path,
    )


@router.get(
    "/dictionary-microservice/api/v2/territories/by-point/related-objects",
    response_model=TerritoryPointSearchWithRecommendationRsDto,
)
async def proxy_get_territories_by_point(
    point_x: float = Query(..., description="Долгота точки"),
    point_y: float = Query(..., description="Широта точки"),
    task_type: str = Query(
        default="agriculture",
        description="Тип задачи рекомендации: agriculture, construction, ecology",
    ),
    target: str | None = Query(
        default=None,
        description="Пользовательская цель рекомендации",
    ),
) -> TerritoryPointSearchWithRecommendationRsDto:
    params_for_log = {
        "point_x": point_x,
        "point_y": point_y,
        "task_type": task_type,
        "target": target,
    }

    logger.debug(
        "START GatewayTerritoryController::proxy_get_territories_by_point %s",
        params_for_log,
    )

    service = TerritoryService()

    result = await service.get_by_point_with_recommendation(
        coord_x=point_x,
        coord_y=point_y,
        task_type=task_type,
        target=target,
    )

    if result is None:
        logger.debug(
            "END GatewayTerritoryController::proxy_get_territories_by_point %s None",
            params_for_log,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Точка не принадлежит ни одной территории.",
        )

    logger.debug(
        "END GatewayTerritoryController::proxy_get_territories_by_point %s %s",
        params_for_log,
        result,
    )

    return result


@router.post(
    "/dictionary-microservice/api/v1/files",
    response_model=FileUploadRsDto,
)
async def proxy_upload_dictionary_file(
    file_group: str = Query(..., description="Группа файла"),
    file: UploadFile = File(...),
) -> FileUploadRsDto:
    params_for_log = {
        "file_group": file_group,
        "filename": file.filename,
        "content_type": file.content_type,
    }

    logger.info(
        "START GatewayFileController::proxy_upload_dictionary_file %s",
        params_for_log,
    )

    if not file_group.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Параметр file_group обязателен.",
        )

    service = FileMetadataService()

    result = await service.save_dictionary_microservice_file(
        file=file,
        file_group=file_group.strip(),
    )

    logger.info(
        "END GatewayFileController::proxy_upload_dictionary_file %s %s",
        params_for_log,
        result,
    )

    return result


@router.get(
    "/dictionary-microservice/api/v1/files/{file_id}",
)
async def proxy_download_dictionary_file(
    file_id: uuid.UUID,
) -> StreamingResponse:
    params_for_log = {
        "file_id": file_id,
    }

    logger.debug(
        "START GatewayFileController::proxy_download_dictionary_file %s",
        params_for_log,
    )

    service = FileMetadataService()

    result = await service.download_dictionary_microservice_file(
        file_id=file_id,
    )

    if result is None:
        logger.debug(
            "END GatewayFileController::proxy_download_dictionary_file %s None",
            params_for_log,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден.",
        )

    logger.debug(
        "END GatewayFileController::proxy_download_dictionary_file %s filename=%s",
        params_for_log,
        result.filename,
    )

    return build_file_response(result)


@router.api_route(
    "/dictionary-microservice/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def proxy_dictionary(
    path: str,
    request: Request,
):
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.dictionary_service_url,
        path="/" + path,
    )


@router.api_route(
    "/ml-microservice/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def proxy_ml(
    path: str,
    request: Request,
):
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ml_service_url,
        path="/" + path,
    )