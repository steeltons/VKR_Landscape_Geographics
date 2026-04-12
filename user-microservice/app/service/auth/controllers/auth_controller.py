from fastapi import APIRouter, Depends

from app.service.auth.auth_dependencies import get_auth_service
from app.service.auth.auth_service import AuthService
from app.service.auth.dto.auth_dto import AuthLoginRqDto, AuthTokenRsDto

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)


@router.post("/login", response_model=AuthTokenRsDto)
def login(body: AuthLoginRqDto, auth_service: AuthService = Depends(get_auth_service),) -> AuthTokenRsDto:
    return auth_service.login(body)