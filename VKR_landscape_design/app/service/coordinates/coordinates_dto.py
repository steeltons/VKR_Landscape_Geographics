from pydantic import BaseModel, ConfigDict


class PolygonPointRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    latitude: float
    longitude: float
    order: int


class PolygonRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    points: list[PolygonPointRsDto]


class TerritoryCoordinatesItemRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    territory_id: int
    color: str
    polygons: list[PolygonRsDto]


class TerritoryCoordinatesRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[TerritoryCoordinatesItemRsDto]