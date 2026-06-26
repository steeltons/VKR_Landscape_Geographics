from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Relief, LandscapeReliefConnection


class ReliefRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, relief_id: int) -> Relief | None:
        stmt = select(Relief).where(
            Relief.id == relief_id,
            Relief.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_all_by_landscape_id(self, landscape_id):
        stmt = (select(Relief)
                .join(LandscapeReliefConnection, LandscapeReliefConnection.relief_id == Relief.id)
                .where(LandscapeReliefConnection.landscape_id == landscape_id)
                .where(Relief.is_active.is_(True))
                .order_by(Relief.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Relief]:
        stmt = (
            select(Relief)
            .where(Relief.is_active.is_(True))
            .order_by(Relief.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Relief) -> Relief:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Relief) -> Relief:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity