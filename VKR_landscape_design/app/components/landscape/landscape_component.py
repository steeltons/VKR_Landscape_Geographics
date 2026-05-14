from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.components.landscape.landscape_component_mapper import LandscapeComponentMapper
from app.components.landscape.landscape_dc import LandscapeDC
from app.persistence.repositories.landscape_repository import LandscapeRepository
from app.persistence.models import Landscape


class LandscapeComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = LandscapeRepository(db)

    def get_by_id(self, landscape_id: int) -> LandscapeDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(landscape_id)
            return LandscapeComponentMapper.to_dc(entity) if entity else None

    def get_all(self) -> list[LandscapeDC]:
        with self.db.begin_nested():
            return LandscapeComponentMapper.to_dc_list(
                self.repository.get_all()
            )

    def create(
        self,
        *,
        name: str,
        code: str | None = None,
        description: str | None = None,
        area_square: Decimal | None = None,
        area_percentage: Decimal | None = None,
        kr: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> LandscapeDC:
        entity = Landscape(
            name=name,
            code=code,
            description=description,
            area_square=area_square,
            area_percentage=area_percentage,
            kr=kr,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            return LandscapeComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        landscape_id: int,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        area_square: Decimal | None = None,
        area_percentage: Decimal | None = None,
        kr: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> LandscapeDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(landscape_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if code is not None:
                entity.code = code
            if description is not None:
                entity.description = description
            if area_square is not None:
                entity.area_square = area_square
            if area_percentage is not None:
                entity.area_percentage = area_percentage
            if kr is not None:
                entity.kr = kr
            if picture_id is not None:
                entity.picture_id = picture_id

            return LandscapeComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, landscape_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(landscape_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True