from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClimateCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class ClimateUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    picture_id: UUID | None = None


class ClimateRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None


class ClimatesRsDto(BaseModel):
    items: list[ClimateRsDto]
    limit: int
    offset: int