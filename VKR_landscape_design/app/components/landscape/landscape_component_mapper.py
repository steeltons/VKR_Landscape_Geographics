from app.components.landscape.landscape_dc import LandscapeDC
from app.persistence.models import Landscape


class LandscapeComponentMapper:
    @staticmethod
    def to_dc(entity: Landscape) -> LandscapeDC:
        return LandscapeDC(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            description=entity.description,
            area_square=entity.area_square,
            area_percentage=entity.area_percentage,
            kr=entity.kr,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Landscape]) -> list[LandscapeDC]:
        return [LandscapeComponentMapper.to_dc(entity) for entity in entities]