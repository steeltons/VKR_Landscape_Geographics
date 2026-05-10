from app.components.soil.soil_dc import SoilDC
from app.persistence.models import Soil


class SoilMapper:
    @staticmethod
    def to_dc(entity: Soil) -> SoilDC:
        return SoilDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            acidity=entity.acidity,
            minerals=entity.minerals,
            profile=entity.profile,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Soil]) -> list[SoilDC]:
        return [SoilMapper.to_dc(entity) for entity in entities]