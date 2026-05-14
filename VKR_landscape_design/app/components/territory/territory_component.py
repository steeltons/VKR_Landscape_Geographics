from sqlalchemy.orm import Session

from app.components.territory.territory_component_mapper import TerritoryComponentMapper
from app.components.territory.territory_dc import TerritoryDC
from app.persistence.models import Territory
from app.persistence.repositories.territory_repository import TerritoryRepository


class TerritoryComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = TerritoryRepository(db)

    def get_by_id(self, territory_id: int) -> TerritoryDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(territory_id)
            return TerritoryComponentMapper.to_dc(entity) if entity else None

    def get_by_point(
            self,
            *,
            point_x: float,
            point_y: float,
    ) -> TerritoryDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_point(
                point_x=point_x,
                point_y=point_y,
            )

            if entity is None:
                return None

            return TerritoryComponentMapper.to_dc(entity)

    def get_all(self) -> list[TerritoryDC]:
        with self.db.begin_nested():
            return TerritoryComponentMapper.to_dc_list(
                self.repository.get_all()
            )

    def create(
        self,
        *,
        description: str | None = None,
        landscape_id: int | None = None,
    ) -> TerritoryDC:
        entity = Territory(
            description=description,
            landscape_id=landscape_id,
            is_active=True,
        )

        with self.db.begin():
            return TerritoryComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        territory_id: int,
        description: str | None = None,
        landscape_id: int | None = None,
    ) -> TerritoryDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(territory_id)
            if entity is None:
                return None

            if description is not None:
                entity.description = description
            if landscape_id is not None:
                entity.landscape_id = landscape_id

            return TerritoryComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, territory_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(territory_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True