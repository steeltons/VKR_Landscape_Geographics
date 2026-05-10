from sqlalchemy.orm import Session

from app.components.coordinates.coordinates_component_mapper import (
    CoordinatesComponentMapper,
)
from app.components.coordinates.coordinates_dc import TerritoryCoordinatesDC
from app.persistence.repositories.territory_geometry_repository import TerritoryGeometryRepository


class CoordinatesComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TerritoryGeometryRepository(db)

    def get_all_coordinates(self) -> TerritoryCoordinatesDC:
        with self.db.begin_nested():
            rows = self.repository.get_all_active_geometries()
            return CoordinatesComponentMapper.to_dc(rows)