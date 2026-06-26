from jwt_guard.model import JwtPrincipal

from app.models.models import UserAuthorityType

def get_login(principal: JwtPrincipal) -> str:
    return principal.login

def get_email(principal: JwtPrincipal) -> str:
    return principal.email

def get_authorities(principal: JwtPrincipal) -> list[UserAuthorityType]:
    authorities = principal.authorities

    return [UserAuthorityType.from_system_name(authority) for authority in authorities]