from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TerritoryCreateParamsRqDto(BaseModel):
    description: str | None = None
    landscape_id: int | None = None


class TerritoryUpdateParamsRqDto(BaseModel):
    description: str | None = None
    landscape_id: int | None = None


class TerritoryRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None
    landscape_id: int | None


class TerritoryPointLandscapeRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str | None
    description: str | None
    area_square: Decimal | None
    area_percentage: Decimal | None
    kr: Decimal | None
    picture_id: UUID | None


class TerritoryPointSoilRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    acidity: Decimal | None
    minerals: str | None
    profile: str | None
    picture_id: UUID | None


class TerritoryPointGroundRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    density: Decimal | None
    humidity: Decimal | None
    solidity: Decimal | None
    picture_id: UUID | None


class TerritoryPointPlantRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None


class TerritoryPointReliefRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None


class TerritoryPointFoundationRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    roof_root_depth: Decimal | None
    picture_id: UUID | None


class TerritoryPointWaterRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None


class TerritoryPointClimateRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    picture_id: UUID | None


class TerritoryPointSearchRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    territory: TerritoryRsDto
    landscape: TerritoryPointLandscapeRsDto | None
    soils: list[TerritoryPointSoilRsDto]
    grounds: list[TerritoryPointGroundRsDto]
    plants: list[TerritoryPointPlantRsDto]
    reliefs: list[TerritoryPointReliefRsDto]
    foundations: list[TerritoryPointFoundationRsDto]
    waters: list[TerritoryPointWaterRsDto]
    climates: list[TerritoryPointClimateRsDto]