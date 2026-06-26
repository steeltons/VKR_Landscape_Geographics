from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.utils.jwt_utils import get_authorities
from app.models.models import UserAuthorityType
from app.core.jwt_guard import require_access_token
from jwt_guard.model import JwtPrincipal

def require_authorities(*required_authorities: UserAuthorityType) -> Callable:

    def dependency(principal: JwtPrincipal = Depends(require_access_token)) -> JwtPrincipal:
        principal_authorities = set(get_authorities(principal))
        required = set(required_authorities)

        if not required.issubset(principal_authorities):
            raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Not enough permissions")

        return principal

    return dependency