from app.components.relief.relief_dc import ReliefDC
from app.persistence.models import Relief


class ReliefComponentMapper:
    @staticmethod
    def to_dc(entity: Relief) -> ReliefDC:
        return ReliefDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Relief]) -> list[ReliefDC]:
        return [ReliefComponentMapper.to_dc(entity) for entity in entities]