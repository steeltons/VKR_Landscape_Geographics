from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Plant, LandscapePlantConnection


class PlantRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, plant_id: int) -> Plant | None:
        stmt = (
            select(Plant)
            .where(Plant.id == plant_id)
            .where(Plant.is_active.is_(True))
        )
        return self.db.scalar(stmt)

    def get_all_by_landscape_id(self, landscape_id: int) -> list[Plant]:
        stmt = (
            select(Plant)
            .join(LandscapePlantConnection, LandscapePlantConnection.plant_id == Plant.id)
            .where(LandscapePlantConnection.landscape_id == landscape_id)
            .where(Plant.is_active.is_(True))
            .order_by(Plant.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Plant]:
        stmt = (
            select(Plant)
            .where(Plant.is_active.is_(True))
            .order_by(Plant.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Plant) -> Plant:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Plant) -> Plant:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity