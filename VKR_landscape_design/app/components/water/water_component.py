from uuid import UUID

from sqlalchemy.orm import Session

from app.components.water.water_component_mapper import WaterComponentMapper
from app.components.water.water_dc import WaterDC
from app.persistence.models import Water
from app.persistence.repositories.water_repository import WaterRepository


class WaterComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = WaterRepository(db)

    def get_by_id(self, water_id: int) -> WaterDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(water_id)
            return WaterComponentMapper.to_dc(entity) if entity else None

    def get_all_by_landscape_id(self, landscape_id: int) -> list[WaterDC]:
        with self.db.begin_nested():
            return WaterComponentMapper.to_dc_list(
                self.repository.get_by_landscape_id(landscape_id)
            )

    def get_all(self) -> list[WaterDC]:
        with self.db.begin_nested():
            return WaterComponentMapper.to_dc_list(
                self.repository.get_all()
            )

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> WaterDC:
        entity = Water(
            name=name,
            description=description,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            return WaterComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        water_id: int,
        name: str | None = None,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> WaterDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(water_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if picture_id is not None:
                entity.picture_id = picture_id

            return WaterComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, water_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(water_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True