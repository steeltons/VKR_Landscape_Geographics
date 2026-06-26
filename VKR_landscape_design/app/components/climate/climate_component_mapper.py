from app.components.climate.climate_dc import ClimateDC
from app.persistence.models import Climate


class ClimateComponentMapper:
    @staticmethod
    def to_dc(entity: Climate) -> ClimateDC:
        return ClimateDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Climate]) -> list[ClimateDC]:
        return [ClimateComponentMapper.to_dc(entity) for entity in entities]