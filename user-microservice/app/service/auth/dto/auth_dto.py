import uuid
from pydantic import BaseModel, EmailStr


class AuthLoginRqDto(BaseModel):
    username: str
    password: str

class AuthLogoutRqDto(BaseModel):
    refresh_token: str

class AuthRefreshRqDto(BaseModel):
    refresh_token: str

class AuthPrincipalDto(BaseModel):
    user_id: uuid.UUID
    login: str
    email: EmailStr


class AuthTokenRsDto(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int