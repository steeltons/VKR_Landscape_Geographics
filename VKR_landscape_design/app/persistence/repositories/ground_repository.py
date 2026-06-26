from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Ground, LandscapeGroundConnection


class GroundRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, ground_id: int) -> Ground | None:
        stmt = (
            select(Ground)
            .where(Ground.id == ground_id)
            .where(Ground.is_active.is_(True))
        )
        return self.db.scalar(stmt)

    def get_all_by_landscape_id(self, landscape_id: int) -> list[Ground]:
        stmt = (
            select(Ground)
            .join(LandscapeGroundConnection, LandscapeGroundConnection.ground_id == Ground.id)
            .where(LandscapeGroundConnection.landscape_id == landscape_id)
            .where(Ground.is_active.is_(True))
            .order_by(Ground.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Ground]:
        stmt = (
            select(Ground)
            .where(Ground.is_active.is_(True))
            .order_by(Ground.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Ground) -> Ground:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Ground) -> Ground:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity