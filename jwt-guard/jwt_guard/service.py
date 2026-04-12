from jose import JWTError, jwt

from .config import JwtGuardConfig
from .exceptions import JwtUnauthorizedException
from .model import JwtPrincipal


class JwtVerifierService:
    def __init__(self, config: JwtGuardConfig):
        self.config = config

    def verify_access_token(self, token: str) -> JwtPrincipal:
        options = {
            "verify_aud": self.config.audience is not None,
            "verify_iss": self.config.issuer is not None,
        }

        try:
            payload = jwt.decode(
                token,
                self.config.public_key,
                algorithms=[self.config.algorithm],
                audience=self.config.audience,
                issuer=self.config.issuer,
                options=options,
            )
        except JWTError as exc:
            raise JwtUnauthorizedException("Invalid or expired token") from exc

        principal = JwtPrincipal.model_validate(payload)

        if principal.type != self.config.token_type:
            raise JwtUnauthorizedException("Invalid token type")

        return principal