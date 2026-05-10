from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Landscape


class LandscapeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, landscape_id: int) -> Landscape | None:
        stmt = select(Landscape).where(
            Landscape.id == landscape_id,
            Landscape.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Landscape]:
        stmt = (
            select(Landscape)
            .where(Landscape.is_active.is_(True))
            .order_by(Landscape.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Landscape) -> Landscape:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Landscape) -> Landscape:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity