import logging

from fastapi import APIRouter, Request, HTTPException
from starlette import status

from app.proxy.client import ProxyClient
from app.configs.config import settings

from app.service.territory_service import TerritoryService
from app.service.territory_recommendation_dto import TerritoryPointSearchWithRecommendationRsDto

logger = logging.getLogger(__name__)

router = APIRouter()

proxy_client = ProxyClient(
    timeout_seconds=settings.request_timeout_seconds,
)


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


@router.get("/dictionary-microservice/api/v2/territories/by-point/related-objects", response_model=TerritoryPointSearchWithRecommendationRsDto)
async def proxy_get_territories_by_point(request: Request) -> TerritoryPointSearchWithRecommendationRsDto:
    query_params = request.query_params

    params_for_log = dict(query_params)

    logger.debug("START GatewayTerritoryController::proxy_get_territories_by_point %s", params_for_log,)

    point_x_raw = query_params.get("point_x")
    point_y_raw = query_params.get("point_y")

    if point_x_raw is None or point_y_raw is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Параметры point_x и point_y обязательны.",
        )

    try:
        point_x = float(point_x_raw)
        point_y = float(point_y_raw)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Параметры point_x и point_y должны быть числами.",
        )

    task_type = query_params.get("task_type", "agriculture")
    target = query_params.get("target")

    service = TerritoryService()

    result = await service.get_by_point_with_recommendation(
        coord_x=point_x,
        coord_y=point_y,
        task_type=task_type,
        target=target,
    )

    if result is None:
        logger.debug("END GatewayTerritoryController::proxy_get_territories_by_point %s None", params_for_log)

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
    "/ml/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def proxy_ml(
    path: str,
    request: Request,
):
    return await proxy_client.forward(
        request=request,
        target_base_url=settings.ml_service_url,
        path=f"/api/v1/{path}",
    )