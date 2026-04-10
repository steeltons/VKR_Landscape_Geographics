from pydantic import BaseModel, ConfigDict


class UserRsDto(BaseModel):

    model_config = ConfigDict(from_attributes= True)

    login: str
    email: str
