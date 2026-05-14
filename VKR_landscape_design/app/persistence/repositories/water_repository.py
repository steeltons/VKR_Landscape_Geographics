from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Water, LandscapeWaterConnection


class WaterRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, water_id: int) -> Water | None:
        stmt = select(Water).where(
            Water.id == water_id,
            Water.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_by_landscape_id(self, landscape_id: int) -> list[Water]:
        stmt = (
            select(Water)
            .join(LandscapeWaterConnection, LandscapeWaterConnection.water_id == Water.id)
            .where(LandscapeWaterConnection.landscape_id == landscape_id)
            .where(Water.is_active.is_(True))
            .order_by(Water.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self) -> list[Water]:
        stmt = (
            select(Water)
            .where(Water.is_active.is_(True))
            .order_by(Water.id)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Water) -> Water:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Water) -> Water:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity