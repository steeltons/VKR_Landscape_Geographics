from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.dependencies import get_db
from app.service.auth.auth_service import AuthService
from app.service.auth.token_service import TokenService


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:

    token_service = TokenService(
        private_key= settings.jwt_private_key,
        algorithm= settings.jwt_algorithm,
        access_token_ttl_minutes= settings.access_token_ttl_minutes,
        refresh_token_ttl_days= settings.refresh_token_ttl_days,
        issuer= settings.jwt_issuer,
        audience= settings.jwt_audience,
    )

    return AuthService(
        db=db,
        token_service=token_service,
    )