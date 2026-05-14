from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.models import Foundation, LandscapeFoundationConnection


class FoundationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, foundation_id: int) -> Foundation | None:
        stmt = select(Foundation).where(
            Foundation.id == foundation_id,
            Foundation.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get_by_landscape_id(self, landscape_id):
        stmt = (
            select(Foundation)
            .join(LandscapeFoundationConnection, LandscapeFoundationConnection.foundation_id == Foundation.id)
            .where(LandscapeFoundationConnection.landscape_id == landscape_id)
            .where(Foundation.is_active.is_(True))
            .order_by(Foundation.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self) -> list[Foundation]:
        stmt = (
            select(Foundation)
            .where(Foundation.is_active.is_(True))
            .order_by(Foundation.id)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Foundation) -> Foundation:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Foundation) -> Foundation:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity