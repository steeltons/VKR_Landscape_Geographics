from fastapi import APIRouter, Request

from app.proxy.client import ProxyClient
from app.configs.config import settings


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