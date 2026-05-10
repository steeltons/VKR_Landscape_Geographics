from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolygonPointDC:
    latitude: float
    longitude: float
    order: int


@dataclass(frozen=True, slots=True)
class PolygonDC:
    points: list[PolygonPointDC]


@dataclass(frozen=True, slots=True)
class TerritoryCoordinatesItemDC:
    territory_id: int
    color: str
    polygons: list[PolygonDC]


@dataclass(frozen=True, slots=True)
class TerritoryCoordinatesDC:
    items: list[TerritoryCoordinatesItemDC]