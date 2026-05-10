from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.components.soil.soil_component_mapper import SoilMapper
from app.components.soil.soil_dc import SoilDC
from app.persistence.models import Soil
from app.persistence.repositories.soil_repository import SoilRepository


class SoilComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = SoilRepository(db)

    def get_by_id(self, soil_id: int) -> SoilDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(soil_id)
            if entity is None:
                return None

            return SoilMapper.to_dc(entity)

    def get_all_by_landscape_id(self, landscape_id: int) -> list[SoilDC] | None:
        with self.db.begin_nested():
            return SoilMapper.to_dc_list(
                self.repository.get_all_by_landscape_id(landscape_id)
            )

    def get_all(self) -> list[SoilDC]:
        with self.db.begin_nested():
            entities = self.repository.get_all()
            return SoilMapper.to_dc_list(entities)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        acidity: Decimal | None = None,
        minerals: str | None = None,
        profile: str | None = None,
        picture_id: UUID | None = None,
    ) -> SoilDC:
        entity = Soil(
            name=name,
            description=description,
            acidity=acidity,
            minerals=minerals,
            profile=profile,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            created_entity = self.repository.create(entity)
            return SoilMapper.to_dc(created_entity)

    def update(
        self,
        *,
        soil_id: int,
        name: str | None = None,
        description: str | None = None,
        acidity: Decimal | None = None,
        minerals: str | None = None,
        profile: str | None = None,
        picture_id: UUID | None = None,
    ) -> SoilDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(soil_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if acidity is not None:
                entity.acidity = acidity
            if minerals is not None:
                entity.minerals = minerals
            if profile is not None:
                entity.profile = profile
            if picture_id is not None:
                entity.picture_id = picture_id

            updated_entity = self.repository.update(entity)
            return SoilMapper.to_dc(updated_entity)

    def deactivate(self, soil_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(soil_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True