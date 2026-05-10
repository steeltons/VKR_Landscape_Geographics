from app.components.ground.ground_dc import GroundDC
from app.persistence.models import Ground


class GroundComponentMapper:
    @staticmethod
    def to_dc(entity: Ground) -> GroundDC:
        return GroundDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            density=entity.density,
            humidity=entity.humidity,
            solidity=entity.solidity,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Ground]) -> list[GroundDC]:
        return [GroundComponentMapper.to_dc(entity) for entity in entities]