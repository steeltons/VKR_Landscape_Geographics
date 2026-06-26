from jwt_guard import JwtGuardConfig, build_require_access_token

from app.core.config import settings


jwt_guard_config = JwtGuardConfig(
    public_key=settings.jwt_public_key,
    algorithm=settings.jwt_algorithm,
    issuer=settings.jwt_issuer,
    audience=settings.jwt_audience,
)

require_access_token = build_require_access_token(jwt_guard_config)