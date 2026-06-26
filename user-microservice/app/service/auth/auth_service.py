from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.service.auth.dto.auth_dto import AuthLoginRqDto, AuthTokenRsDto, AuthLogoutRqDto, AuthRefreshRqDto
from app.service.auth.password_service import authenticate, get_principal_by_user_id
from app.service.auth.refresh_session_service import create_session, revoke_session_by_refresh_token, get_valid_session_by_refresh_token, rotate_session
from app.service.auth.token_service import TokenService

from app.models.models import UserAuthority, UserProfile


class AuthService:
    def __init__(
        self,
        db: Session,
        token_service: TokenService,
    ):
        self.db = db
        self.token_service = token_service

    def login(self, rq: AuthLoginRqDto) -> AuthTokenRsDto:
        principal = authenticate(db= self.db, login= rq.username, password= rq.password)

        if principal is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        authorities = self.__get_user_authorities(user_id= principal.user_id)
        user_profile = self.__get_user_profile(user_id= principal.user_id)

        access_token, expires_in = self.token_service.create_access_token(principal, user_profile, authorities)
        refresh_token, token_id, refresh_expires_at = self.token_service.create_refresh_token()

        create_session(db= self.db, user_id= principal.user_id, token_id= token_id, raw_refresh_token= refresh_token, expires_at= refresh_expires_at)

        self.db.commit()

        return AuthTokenRsDto(
            access_token= access_token,
            refresh_token= refresh_token,
            expires_in= expires_in,
        )

    def refresh(self, rq: AuthRefreshRqDto) -> AuthTokenRsDto:
        current_session = get_valid_session_by_refresh_token(db= self.db, raw_refresh_token= rq.refresh_token)

        if current_session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        principal = get_principal_by_user_id(db= self.db, user_id= current_session.user_id)

        if principal is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        authorities = self.__get_user_authorities(user_id= principal.user_id)
        user_profile = self.__get_user_profile(user_id= principal.user_id)

        access_token, expires_in = self.token_service.create_access_token(principal, user_profile, authorities)
        new_refresh_token, new_token_id, new_refresh_expires_at = self.token_service.create_refresh_token()

        rotate_session(
            db=self.db,
            current_session=current_session,
            new_token_id=new_token_id,
            new_raw_refresh_token=new_refresh_token,
            new_expires_at=new_refresh_expires_at,
        )

        self.db.commit()

        return AuthTokenRsDto(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=expires_in,
        )

    def logout(self, rq: AuthLogoutRqDto) -> None:
        revoke_session_by_refresh_token(db= self.db, raw_refresh_token= rq.refresh_token)
        self.db.commit()

    def __get_user_authorities(self, user_id : UUID):
        user_authorities = (self.db.query(UserAuthority)
                            .where((UserAuthority.user_id == user_id) &
                                   (UserAuthority.is_active.is_(True)))
                            .all())

        return [user_authority.authority.system_name for user_authority in user_authorities]

    def __get_user_profile(self, user_id : UUID) -> UserProfile | None:
        return (self.db.query(UserProfile)
                .filter(UserProfile.user_id == user_id)
                .filter(UserProfile.is_active.is_(True))
                .first())
