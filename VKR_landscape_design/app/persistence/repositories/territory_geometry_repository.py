from typing import NamedTuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.persistence.models import TerritoryGeometry


class TerritoryGeometryRow(NamedTuple):
    territory_id: int
    geojson: str
    color: str


class TerritoryGeometryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_active_geometries(self) -> list[TerritoryGeometryRow]:
        stmt = (
            select(
                TerritoryGeometry.territory_id,
                TerritoryGeometry.color,
                func.ST_AsGeoJSON(TerritoryGeometry.geom).label("geojson"),
            )
            .where(TerritoryGeometry.is_active.is_(True))
            .order_by(TerritoryGeometry.territory_id)
        )

        rows = self.db.execute(stmt).all()

        return [
            TerritoryGeometryRow(
                territory_id=row.territory_id,
                color= row.color,
                geojson=row.geojson,
            )
            for row in rows
        ]