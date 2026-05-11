from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TerritoryRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None
    landscape_id: int | None
    is_active: bool


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

class TerritoryRecommendationEvidenceRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    object_type: str
    object_id: int
    title: str
    api_path: str
    impact: str
    factor: str
    reason: str


class TerritoryRecommendationExplanationRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary: str
    reasons: list[str]
    warnings: list[str]
    evidence: list[TerritoryRecommendationEvidenceRsDto]

class TerritoryRecommendationRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    score: float
    level: str
    recommendation: str
    explanation: TerritoryRecommendationExplanationRsDto

class TerritoryPointSearchWithRecommendationRsDto(BaseModel):
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
    recommendation: TerritoryRecommendationRsDto | None = None
