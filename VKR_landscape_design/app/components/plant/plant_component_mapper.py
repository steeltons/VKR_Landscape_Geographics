from app.components.plant.plant_dc import PlantDC
from app.persistence.models import Plant


class PlantComponentMapper:
    @staticmethod
    def to_dc(entity: Plant) -> PlantDC:
        return PlantDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Plant]) -> list[PlantDC]:
        return [PlantComponentMapper.to_dc(entity) for entity in entities]