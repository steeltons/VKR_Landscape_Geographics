from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.components.foundation.foundation_component_mapper import FoundationComponentMapper
from app.components.foundation.foundation_dc import FoundationDC
from app.persistence.repositories.foundation_repository import FoundationRepository
from app.persistence.models import Foundation


class FoundationComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = FoundationRepository(db)

    def get_by_id(self, foundation_id: int) -> FoundationDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(foundation_id)
            return FoundationComponentMapper.to_dc(entity) if entity else None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[FoundationDC]:
        with self.db.begin_nested():
            return FoundationComponentMapper.to_dc_list(
                self.repository.get_all(limit=limit, offset=offset)
            )

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        roof_root_depth: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> FoundationDC:
        entity = Foundation(
            name=name,
            description=description,
            roof_root_depth=roof_root_depth,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            return FoundationComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        foundation_id: int,
        name: str | None = None,
        description: str | None = None,
        roof_root_depth: Decimal | None = None,
        picture_id: UUID | None = None,
    ) -> FoundationDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(foundation_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if roof_root_depth is not None:
                entity.roof_root_depth = roof_root_depth
            if picture_id is not None:
                entity.picture_id = picture_id

            return FoundationComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, foundation_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(foundation_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True