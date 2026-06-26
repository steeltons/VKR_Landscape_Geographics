from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FoundationCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    roof_root_depth: Decimal | None = None
    picture_id: UUID | None = None


class FoundationUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    roof_root_depth: Decimal | None = None
    picture_id: UUID | None = None


class FoundationRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    roof_root_depth: Decimal | None
    picture_id: UUID | None