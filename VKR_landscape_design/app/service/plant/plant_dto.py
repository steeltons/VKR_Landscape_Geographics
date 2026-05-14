from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PlantCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class PlantUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class PlantRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None
    is_active: bool
