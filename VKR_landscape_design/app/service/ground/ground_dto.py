from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GroundCreateParamsRqDto(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    density: Decimal | None = None
    humidity: Decimal | None = None
    solidity: Decimal | None = None
    picture_id: UUID | None = None


class GroundUpdateParamsRqDto(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    density: Decimal | None = None
    humidity: Decimal | None = None
    solidity: Decimal | None = None
    picture_id: UUID | None = None


class GroundRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    density: Decimal | None
    humidity: Decimal | None
    solidity: Decimal | None
    picture_id: UUID | None
    is_active: bool


class GroundsRsDto(BaseModel):
    items: list[GroundRsDto]
    limit: int
    offset: int