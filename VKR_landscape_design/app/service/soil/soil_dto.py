from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SoilCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    acidity: Decimal | None = None
    minerals: str | None = None
    profile: str | None = None
    picture_id: UUID | None = None


class SoilUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    acidity: Decimal | None = None
    minerals: str | None = None
    profile: str | None = None
    picture_id: UUID | None = None


class SoilRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    acidity: Decimal | None
    minerals: str | None
    profile: str | None
    picture_id: UUID | None
    is_active: bool