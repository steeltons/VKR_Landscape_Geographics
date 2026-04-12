from fastapi import APIRouter, Depends, Response, status

from app.service.auth.auth_dependencies import get_auth_service
from app.service.auth.auth_service import AuthService
from app.service.auth.dto.auth_dto import AuthLoginRqDto, AuthTokenRsDto, AuthLogoutRqDto, AuthRefreshRqDto

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.post("/login", response_model=AuthTokenRsDto)
def login(body: AuthLoginRqDto, auth_service: AuthService = Depends(get_auth_service),) -> AuthTokenRsDto:
    return auth_service.login(body)

@router.post("/logout", status_code= status.HTTP_204_NO_CONTENT)
def logout(body: AuthLogoutRqDto, auth_service: AuthService = Depends(get_auth_service)) -> Response:
    auth_service.logout(body)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/refresh", response_model=AuthTokenRsDto)
def refresh(body: AuthRefreshRqDto, auth_service: AuthService = Depends(get_auth_service)) -> AuthTokenRsDto:
    return auth_service.refresh(body)