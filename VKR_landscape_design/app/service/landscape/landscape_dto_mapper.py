from app.components.landscape.landscape_dc import LandscapeDC
from app.service.landscape.landscape_dto import LandscapeRsDto, LandscapesRsDto


class LandscapeDtoMapper:
    @staticmethod
    def to_rs_dto(dc: LandscapeDC) -> LandscapeRsDto:
        return LandscapeRsDto(**dc.__dict__)

    @staticmethod
    def to_list_rs_dto(
        items: list[LandscapeDC],
        *,
        limit: int,
        offset: int,
    ) -> LandscapesRsDto:
        return LandscapesRsDto(
            items=[LandscapeDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )