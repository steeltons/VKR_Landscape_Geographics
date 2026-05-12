from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.components.ground.ground_component_mapper import GroundComponentMapper
from app.components.ground.ground_dc import GroundDC
from app.persistence.models import Ground
from app.persistence.repositories.ground_repository import GroundRepository


class GroundComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = GroundRepository(db)

    def get_by_id(self, ground_id: int) -> GroundDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(ground_id)
            if entity is None:
                return None
            return GroundComponentMapper.to_dc(entity)

    def get_all_by_landscape_id(self, landscape_id: int) -> list[GroundDC]:
        with self.db.begin_nested():
            return GroundComponentMapper.to_dc_list(
                self.repository.get_all_by_landscape_id(landscape_id)
            )

    def get_all(self) -> list[GroundDC]:
        with self.db.begin_nested():
            entities = self.repository.get_all()
            return GroundComponentMapper.to_dc_list(entities)

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        density: Decimal | None = None,
        humidity: Decimal | None = None,
        solidity: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> GroundDC:
        entity = Ground(
            name=name,
            description=description,
            density=density,
            humidity=humidity,
            solidity=solidity,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            created_entity = self.repository.create(entity)
            return GroundComponentMapper.to_dc(created_entity)

    def update(
        self,
        *,
        ground_id: int,
        name: str | None = None,
        description: str | None = None,
        density: Decimal | None = None,
        humidity: Decimal | None = None,
        solidity: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> GroundDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(ground_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if density is not None:
                entity.density = density
            if humidity is not None:
                entity.humidity = humidity
            if solidity is not None:
                entity.solidity = solidity
            if picture_id is not None:
                entity.picture_id = picture_id

            updated_entity = self.repository.update(entity)
            return GroundComponentMapper.to_dc(updated_entity)

    def deactivate(self, ground_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(ground_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True
