from uuid import UUID

from sqlalchemy.orm import Session

from app.components.plant.plant_component_mapper import PlantComponentMapper
from app.components.plant.plant_dc import PlantDC
from app.persistence.models import Plant
from app.persistence.repositories.plant_repository import PlantRepository


class PlantComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = PlantRepository(db)

    def get_by_id(self, plant_id: int) -> PlantDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(plant_id)
            if entity is None:
                return None
            return PlantComponentMapper.to_dc(entity)

    def get_all_by_landscape_id(self, landscape_id: int) -> list[PlantDC]:
        with self.db.begin_nested():
            return PlantComponentMapper.to_dc_list(
                self.repository.get_all_by_landscape_id(landscape_id)
            )

    def get_all(self, limit: int = 100, offset: int = 0) -> list[PlantDC]:
        with self.db.begin_nested():
            entities = self.repository.get_all(limit=limit, offset=offset)
            return PlantComponentMapper.to_dc_list(entities)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> PlantDC:
        entity = Plant(
            name=name,
            description=description,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            created_entity = self.repository.create(entity)
            return PlantComponentMapper.to_dc(created_entity)

    def update(
        self,
        *,
        plant_id: int,
        name: str | None = None,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> PlantDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(plant_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if picture_id is not None:
                entity.picture_id = picture_id

            updated_entity = self.repository.update(entity)
            return PlantComponentMapper.to_dc(updated_entity)

    def deactivate(self, plant_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(plant_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True