from uuid import UUID

from sqlalchemy.orm import Session

from app.components.climate.climate_component_mapper import ClimateComponentMapper
from app.components.climate.climate_dc import ClimateDC
from app.persistence.models import Climate
from app.persistence.repositories.climate_repository import ClimateRepository


class ClimateComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ClimateRepository(db)

    def get_by_id(self, climate_id: int) -> ClimateDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(climate_id)
            return ClimateComponentMapper.to_dc(entity) if entity else None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[ClimateDC]:
        with self.db.begin_nested():
            return ClimateComponentMapper.to_dc_list(
                self.repository.get_all(limit=limit, offset=offset)
            )

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> ClimateDC:
        entity = Climate(
            name=name,
            description=description,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            return ClimateComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        climate_id: int,
        name: str | None = None,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> ClimateDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(climate_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if picture_id is not None:
                entity.picture_id = picture_id

            return ClimateComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, climate_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(climate_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True