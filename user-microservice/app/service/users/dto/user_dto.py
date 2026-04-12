from pydantic import BaseModel, ConfigDict, Field

from app.models.models import UserAuthorityType


class UserRsDto(BaseModel):

    model_config = ConfigDict(from_attributes= True)

    login: str
    email: str

class AddUserRqDto(BaseModel):

    login: str
    email: str
    password: str

class UserAuthoritiesRqDto(BaseModel):

    model_config = ConfigDict(from_attributes= True)

    authorities: list[UserAuthorityType] = Field(default_factory= list)

