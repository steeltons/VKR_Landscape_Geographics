from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WaterCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class WaterUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class WaterRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra= 'ignore')

    id: int
    name: str
    description: str | None
    picture_id: UUID | None