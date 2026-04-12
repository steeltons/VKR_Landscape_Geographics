from pydantic import BaseModel, ConfigDict


class JwtGuardConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")

    public_key: str
    algorithm: str = "RS256"
    issuer: str | None = None
    audience: str | None = None
    token_type: str = "access"