import uuid
from pydantic import BaseModel, EmailStr


class AuthLoginRqDto(BaseModel):
    login: str
    password: str


class AuthPrincipalDto(BaseModel):
    user_id: uuid.UUID
    login: str
    email: EmailStr


class AuthTokenRsDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int