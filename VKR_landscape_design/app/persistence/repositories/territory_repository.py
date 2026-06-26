from sqlalchemy import select, func, cast, Float
from sqlalchemy.orm import Session

from app.persistence.models import Territory, TerritoryGeometry


class TerritoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, territory_id: int) -> Territory | None:
        stmt = select(Territory).where(
            Territory.id == territory_id,
            Territory.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_all(self) -> list[Territory]:
        stmt = (
            select(Territory)
            .where(Territory.is_active.is_(True))
            .order_by(Territory.id)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Territory) -> Territory:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Territory) -> Territory:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def get_by_point(
            self,
            *,
            point_x: float,
            point_y: float,
    ) -> Territory | None:
        point = func.ST_SetSRID(
            func.ST_Point(
                cast(point_x, Float),
                cast(point_y, Float),
            ),
            4326,
        )

        stmt = (
            select(Territory)
            .join(
                TerritoryGeometry,
                TerritoryGeometry.territory_id == Territory.id,
            )
            .where(Territory.is_active.is_(True))
            .where(TerritoryGeometry.is_active.is_(True))
            .where(func.ST_Contains(TerritoryGeometry.geom, point))
            .order_by(Territory.id)
            .limit(1)
        )

        return self.db.scalar(stmt)