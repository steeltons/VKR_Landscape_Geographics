from app.components.landscape.landscape_dc import LandscapeDC
from app.service.landscape.landscape_dto import LandscapeRsDto


class LandscapeDtoMapper:

    @staticmethod
    def to_rs_dto(dc: LandscapeDC) -> LandscapeRsDto:
        return LandscapeRsDto(
            id= dc.id,
            name = dc.name,
            description = dc.description,
            area_square= dc.area_square,
            area_percentage= dc.area_percentage,
            kr= dc.kr,
            picture_id= dc.picture_id,
            code= dc.code,
        )

    @staticmethod
    def to_list_rs_dto(items: list[LandscapeDC]) -> list[LandscapeRsDto]:
        return [LandscapeDtoMapper.to_rs_dto(item) for item in items]