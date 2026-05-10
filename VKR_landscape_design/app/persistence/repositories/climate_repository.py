from sqlalchemy import select
from sqlalchemy.orm import Session

from app.components.landscape.landscape_component import LandscapeComponent
from app.persistence.models import Climate, LandscapeClimateConnection


class ClimateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, climate_id: int) -> Climate | None:
        stmt = select(Climate).where(
            Climate.id == climate_id,
            Climate.is_active.is_(True),
        )
        return self.db.scalar(stmt)

    def get__all_by_landscape_id(self, landscape_id: int) -> list[Climate] | None:
        stmt = (
            select(Climate)
            .join(
                LandscapeClimateConnection,
                LandscapeClimateConnection.climate_id == Climate.id,
            )
            .where(LandscapeClimateConnection.landscape_id == landscape_id)
            .where(Climate.is_active.is_(True))
            .order_by(Climate.created_at)
        )

        return list(self.db.scalars(stmt).all())

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Climate]:
        stmt = (
            select(Climate)
            .where(Climate.is_active.is_(True))
            .order_by(Climate.id)
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt).all())

    def create(self, entity: Climate) -> Climate:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Climate) -> Climate:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity