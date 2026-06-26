from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Soil, LandscapeSoilConnection


class SoilRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, soil_id: int) -> Soil | None:
        stmt = (
            select(Soil)
            .where(Soil.id == soil_id)
            .where(Soil.is_active.is_(True))
        )
        return self.db.scalar(stmt)

    def get_all_by_landscape_id(self, landscape_id):
        stmt = (
            select(Soil)
            .join(LandscapeSoilConnection, LandscapeSoilConnection.soil_id == Soil.id)
            .where(LandscapeSoilConnection.landscape_id == landscape_id)
            .where(Soil.is_active.is_(True))
            .order_by(Soil.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Soil]:
        stmt = (
            select(Soil)
            .where(Soil.is_active.is_(True))
            .order_by(Soil.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Soil) -> Soil:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Soil) -> Soil:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity