from app.components.territory.territory_dc import TerritoryDC
from app.service.territory.territory_dto import TerritoryRsDto, TerritoriesRsDto


class TerritoryDtoMapper:
    @staticmethod
    def to_rs_dto(dc: TerritoryDC) -> TerritoryRsDto:
        return TerritoryRsDto(**dc.__dict__)

    @staticmethod
    def to_list_rs_dto(
        items: list[TerritoryDC],
        *,
        limit: int,
        offset: int,
    ) -> TerritoriesRsDto:
        return TerritoriesRsDto(
            items=[TerritoryDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )