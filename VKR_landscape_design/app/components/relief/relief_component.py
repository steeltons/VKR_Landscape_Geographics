from uuid import UUID

from sqlalchemy.orm import Session

from app.components.relief.relief_component_mapper import ReliefComponentMapper
from app.components.relief.relief_dc import ReliefDC
from app.persistence.models import Relief
from app.persistence.repositories.relief_repository import ReliefRepository


class ReliefComponent:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ReliefRepository(db)

    def get_by_id(self, relief_id: int) -> ReliefDC | None:
        with self.db.begin_nested():
            entity = self.repository.get_by_id(relief_id)
            return ReliefComponentMapper.to_dc(entity) if entity else None

    def get_all(self, limit: int = 100, offset: int = 0) -> list[ReliefDC]:
        with self.db.begin_nested():
            return ReliefComponentMapper.to_dc_list(
                self.repository.get_all(limit=limit, offset=offset)
            )

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> ReliefDC:
        entity = Relief(
            name=name,
            description=description,
            picture_id=picture_id,
            is_active=True,
        )

        with self.db.begin():
            return ReliefComponentMapper.to_dc(self.repository.create(entity))

    def update(
        self,
        *,
        relief_id: int,
        name: str | None = None,
        description: str | None = None,
        picture_id: UUID | None = None,
    ) -> ReliefDC | None:
        with self.db.begin():
            entity = self.repository.get_by_id(relief_id)
            if entity is None:
                return None

            if name is not None:
                entity.name = name
            if description is not None:
                entity.description = description
            if picture_id is not None:
                entity.picture_id = picture_id

            return ReliefComponentMapper.to_dc(self.repository.update(entity))

    def deactivate(self, relief_id: int) -> bool:
        with self.db.begin():
            entity = self.repository.get_by_id(relief_id)
            if entity is None:
                return False

            entity.is_active = False
            self.repository.update(entity)
            return True