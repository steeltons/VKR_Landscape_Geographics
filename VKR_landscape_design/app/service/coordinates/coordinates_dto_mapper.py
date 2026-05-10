from dataclasses import asdict

from app.components.coordinates.coordinates_dc import TerritoryCoordinatesDC
from app.service.coordinates.coordinates_dto import TerritoryCoordinatesRsDto


class CoordinatesDtoMapper:
    @staticmethod
    def to_rs_dto(dc: TerritoryCoordinatesDC) -> TerritoryCoordinatesRsDto:
        return TerritoryCoordinatesRsDto(**asdict(dc))