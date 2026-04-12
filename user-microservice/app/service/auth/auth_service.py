from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.service.auth.dto.auth_dto import AuthLoginRqDto, AuthTokenRsDto
from app.service.auth.password_service import authenticate
from app.service.auth.refresh_session_service import create_session
from app.service.auth.token_service import TokenService


class AuthService:
    def __init__(
        self,
        db: Session,
        token_service: TokenService,
    ):
        self.db = db
        self.token_service = token_service

    def login(self, rq: AuthLoginRqDto) -> AuthTokenRsDto:
        principal = authenticate(db= self.db, login= rq.login, password= rq.password)

        if principal is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token, expires_in = self.token_service.create_access_token(principal)
        refresh_token, token_id, refresh_expires_at = self.token_service.create_refresh_token()

        create_session(db= self.db, user_id= principal.user_id, token_id= token_id, raw_refresh_token= refresh_token, expires_at= refresh_expires_at)

        self.db.commit()

        return AuthTokenRsDto(
            access_token= access_token,
            refresh_token= refresh_token,
            expires_in= expires_in,
        )