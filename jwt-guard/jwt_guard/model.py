from pydantic import BaseModel, ConfigDict, Field

class JwtPrincipal(BaseModel):
    model_config = ConfigDict(extra= 'ignore')

    sub: str
    type: str
    exp: int
    iat: int
    jti: str | None = None
    login: str | None = None
    email: str | None = None
    authorities: list[str] = Field(default_factory= list)