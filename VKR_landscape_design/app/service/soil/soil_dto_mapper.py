from app.components.soil.soil_dc import SoilDC
from app.service.soil.dto.soil_dto import SoilsRsDto, SoilRsDto


class SoilDtoMapper:
    @staticmethod
    def to_rs_dto(dc: SoilDC) -> SoilRsDto:
        return SoilRsDto(
            id=dc.id,
            name=dc.name,
            description=dc.description,
            acidity=dc.acidity,
            minerals=dc.minerals,
            profile=dc.profile,
            picture_id=dc.picture_id,
            is_active=dc.is_active,
        )

    @staticmethod
    def to_list_rs_dto(
        items: list[SoilDC],
        *,
        limit: int,
        offset: int,
    ) -> SoilsRsDto:
        return SoilsRsDto(
            items=[SoilDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )