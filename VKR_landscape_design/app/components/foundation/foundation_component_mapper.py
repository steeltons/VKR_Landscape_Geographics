from app.components.foundation.foundation_dc import FoundationDC
from app.persistence.models import Foundation


class FoundationComponentMapper:
    @staticmethod
    def to_dc(entity: Foundation) -> FoundationDC:
        return FoundationDC(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            roof_root_depth=entity.roof_root_depth,
            picture_id=entity.picture_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Foundation]) -> list[FoundationDC]:
        return [FoundationComponentMapper.to_dc(entity) for entity in entities]