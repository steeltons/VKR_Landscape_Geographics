from app.components.water.water_dc import WaterDC
from app.service.water.water_dto import WaterRsDto


class WaterDtoMapper:

    @staticmethod
    def to_rs_dto(dc: WaterDC) -> WaterRsDto:
        return WaterRsDto(
            id= dc.id,
            name = dc.name,
            description = dc.description,
            picture_id= dc.picture_id,
        )

    @staticmethod
    def to_list_rs_dto(items: list[WaterDC]) -> list[WaterRsDto]:
        return [WaterDtoMapper.to_rs_dto(item) for item in items]
