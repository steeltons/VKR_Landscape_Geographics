from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LandscapeCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    code: str | None = None
    description: str | None = None
    area_square: Decimal | None = None
    area_percentage: Decimal | None = None
    kr: Decimal | None = None
    picture_id: UUID | None = None


class LandscapeUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    code: str | None = None
    description: str | None = None
    area_square: Decimal | None = None
    area_percentage: Decimal | None = None
    kr: Decimal | None = None
    picture_id: UUID | None = None


class LandscapeRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str | None
    description: str | None
    area_square: Decimal | None
    area_percentage: Decimal | None
    kr: Decimal | None
    picture_id: UUID | None