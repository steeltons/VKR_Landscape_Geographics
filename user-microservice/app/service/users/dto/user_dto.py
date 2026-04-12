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

class FullyCreateUserRqDto(BaseModel):

    login: str
    email: str
    password: str
    authorities: list[UserAuthorityType] = Field(default_factory= list)

    first_name: str = Field(default_factory= str)
    last_name: str = Field(default_factory= str)
    middle_name: str = Field(default_factory= str)
    age: int = Field(default_factory= int)
    gender: str = Field(default_factory= str)
