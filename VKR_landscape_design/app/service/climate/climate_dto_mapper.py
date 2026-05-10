from dataclasses import asdict

from app.components.climate.climate_dc import ClimateDC
from app.service.climate.climate_dto import ClimateRsDto, ClimatesRsDto


class ClimateDtoMapper:
    @staticmethod
    def to_rs_dto(dc: ClimateDC) -> ClimateRsDto:
        return ClimateRsDto(**asdict(dc))

    @staticmethod
    def to_list_rs_dto(
        items: list[ClimateDC],
        *,
        limit: int,
        offset: int,
    ) -> ClimatesRsDto:
        return ClimatesRsDto(
            items=[ClimateDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )