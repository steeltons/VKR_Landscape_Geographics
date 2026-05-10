from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Territory


class TerritoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, territory_id: int) -> Territory | None:
        stmt = select(Territory).where(
            Territory.id == territory_id,
            Territory.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Territory]:
        stmt = (
            select(Territory)
            .where(Territory.is_active.is_(True))
            .order_by(Territory.id)
            .limit(limit)
            .offset(offset)
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