from app.components.water.water_dc import WaterDC
from app.persistence.models import Water


class WaterComponentMapper:
    @staticmethod
    def to_dc(entity: Water) -> WaterDC:
        return WaterDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Water]) -> list[WaterDC]:
        return [WaterComponentMapper.to_dc(entity) for entity in entities]