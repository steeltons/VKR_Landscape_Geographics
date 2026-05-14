from app.components.soil.soil_dc import SoilDC
from app.service.soil.soil_dto import SoilRsDto


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
    def to_list_rs_dto(items: list[SoilDC]) -> list[SoilRsDto]:
        return [SoilDtoMapper.to_rs_dto(item) for item in items]