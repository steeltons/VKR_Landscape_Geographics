from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Water


class WaterRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, water_id: int) -> Water | None:
        stmt = select(Water).where(
            Water.id == water_id,
            Water.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Water]:
        stmt = (
            select(Water)
            .where(Water.is_active.is_(True))
            .order_by(Water.id)
            .limit(limit)
            .offset(offset)
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