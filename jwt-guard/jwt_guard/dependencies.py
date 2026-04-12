from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import JwtGuardConfig
from .model import JwtPrincipal
from .exceptions import JwtUnauthorizedException
from .service import JwtVerifierService


bearer_scheme = HTTPBearer(auto_error=False)


def build_require_access_token(config: JwtGuardConfig) -> Callable:
    verifier = JwtVerifierService(config)

    def require_access_token(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]) -> JwtPrincipal:
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise JwtUnauthorizedException("Missing bearer token")

        return verifier.verify_access_token(credentials.credentials)

    return require_access_token