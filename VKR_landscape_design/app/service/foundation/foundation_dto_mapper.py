from app.components.foundation.foundation_dc import FoundationDC
from app.service.foundation.foundation_dto import FoundationRsDto


class FoundationDtoMapper:
    @staticmethod
    def to_rs_dto(dc: FoundationDC) -> FoundationRsDto:
        return FoundationRsDto(
            id= dc.id,
            name= dc.name,
            description= dc.description,
            picture_id= dc.picture_id,
            roof_root_depth = dc.roof_root_depth,
        )

    @staticmethod
    def to_list_rs_dto(items: list[FoundationDC]) -> list[FoundationRsDto]:
        return [FoundationDtoMapper.to_rs_dto(item) for item in items]