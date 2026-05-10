from app.components.water.water_dc import WaterDC
from app.service.water.water_dto import WaterRsDto, WatersRsDto


class WaterDtoMapper:
    @staticmethod
    def to_rs_dto(dc: WaterDC) -> WaterRsDto:
        return WaterRsDto(**dc.__dict__)

    @staticmethod
    def to_list_rs_dto(
        items: list[WaterDC],
        *,
        limit: int,
        offset: int,
    ) -> WatersRsDto:
        return WatersRsDto(
            items=[WaterDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )