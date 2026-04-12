import secrets
import uuid
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.service.auth.dto.auth_dto import AuthPrincipalDto

class TokenService:

    def __init__(
        self,
        private_key: str,
        algorithm: str = "RS256",
        access_token_ttl_minutes: int = 15,
        refresh_token_ttl_days: int = 30,
        issuer: str | None = None,
        audience: str | None = None,
    ):
        self.private_key = private_key
        self.algorithm = algorithm
        self.access_token_ttl_minutes = access_token_ttl_minutes
        self.refresh_token_ttl_days = refresh_token_ttl_days
        self.issuer = issuer
        self.audience = audience

    def create_access_token(self, principal: AuthPrincipalDto) -> tuple[str, int]:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes= self.access_token_ttl_minutes)

        payload = {
            "sub": str(principal.user_id),
            "login": principal.login,
            "email": principal.email,
            "type": "access",
            "iat": int(now.timestamp()),
            "exp": int(expires_at.timestamp()),
        }

        if self.issuer is not None:
            payload["iss"] = self.issuer

        if self.audience is not None:
            payload["audience"] = self.audience

        token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return token, self.access_token_ttl_minutes * 60

    def create_refresh_token(self) -> tuple[str, uuid.UUID, datetime]:
        raw_token = secrets.token_urlsafe(64)
        token_id = uuid.uuid4()
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_ttl_days)
        return raw_token, token_id, expires_at