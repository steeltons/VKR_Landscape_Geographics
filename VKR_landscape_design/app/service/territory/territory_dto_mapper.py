from dataclasses import asdict

from app.components.climate.climate_dc import ClimateDC
from app.components.foundation.foundation_dc import FoundationDC
from app.components.ground.ground_dc import GroundDC
from app.components.landscape.landscape_dc import LandscapeDC
from app.components.plant.plant_dc import PlantDC
from app.components.relief.relief_dc import ReliefDC
from app.components.soil.soil_dc import SoilDC
from app.components.territory.territory_dc import TerritoryDC
from app.components.water.water_dc import WaterDC
from app.service.territory.territory_dto import (
    TerritoryPointClimateRsDto,
    TerritoryPointFoundationRsDto,
    TerritoryPointGroundRsDto,
    TerritoryPointLandscapeRsDto,
    TerritoryPointPlantRsDto,
    TerritoryPointReliefRsDto,
    TerritoryPointSearchRsDto,
    TerritoryPointSoilRsDto,
    TerritoryPointWaterRsDto,
    TerritoryRsDto,
)


class TerritoryDtoMapper:
    @staticmethod
    def to_rs_dto(dc: TerritoryDC) -> TerritoryRsDto:
        return TerritoryRsDto(**asdict(dc))

    @staticmethod
    def to_list_rs_dto(items: list[TerritoryDC]) -> list[TerritoryRsDto]:
        return [TerritoryDtoMapper.to_rs_dto(item) for item in items]

    @staticmethod
    def to_point_search_rs_dto(
        *,
        territory: TerritoryDC,
        landscape: LandscapeDC | None,
        soils: list[SoilDC],
        grounds: list[GroundDC],
        plants: list[PlantDC],
        reliefs: list[ReliefDC],
        foundations: list[FoundationDC],
        waters: list[WaterDC],
        climates: list[ClimateDC],
    ) -> TerritoryPointSearchRsDto:
        return TerritoryPointSearchRsDto(
            territory=TerritoryDtoMapper.to_rs_dto(territory),
            landscape=(
                TerritoryDtoMapper.to_point_landscape_rs_dto(landscape)
                if landscape is not None
                else None
            ),
            soils=[
                TerritoryDtoMapper.to_point_soil_rs_dto(item)
                for item in soils
            ],
            grounds=[
                TerritoryDtoMapper.to_point_ground_rs_dto(item)
                for item in grounds
            ],
            plants=[
                TerritoryDtoMapper.to_point_plant_rs_dto(item)
                for item in plants
            ],
            reliefs=[
                TerritoryDtoMapper.to_point_relief_rs_dto(item)
                for item in reliefs
            ],
            foundations=[
                TerritoryDtoMapper.to_point_foundation_rs_dto(item)
                for item in foundations
            ],
            waters=[
                TerritoryDtoMapper.to_point_water_rs_dto(item)
                for item in waters
            ],
            climates=[
                TerritoryDtoMapper.to_point_climate_rs_dto(item)
                for item in climates
            ],
        )

    @staticmethod
    def to_point_landscape_rs_dto(dc: LandscapeDC) -> TerritoryPointLandscapeRsDto:
        return TerritoryPointLandscapeRsDto(**asdict(dc))

    @staticmethod
    def to_point_soil_rs_dto(dc: SoilDC) -> TerritoryPointSoilRsDto:
        return TerritoryPointSoilRsDto(**asdict(dc))

    @staticmethod
    def to_point_ground_rs_dto(dc: GroundDC) -> TerritoryPointGroundRsDto:
        return TerritoryPointGroundRsDto(**asdict(dc))

    @staticmethod
    def to_point_plant_rs_dto(dc: PlantDC) -> TerritoryPointPlantRsDto:
        return TerritoryPointPlantRsDto(**asdict(dc))

    @staticmethod
    def to_point_relief_rs_dto(dc: ReliefDC) -> TerritoryPointReliefRsDto:
        return TerritoryPointReliefRsDto(**asdict(dc))

    @staticmethod
    def to_point_foundation_rs_dto(dc: FoundationDC) -> TerritoryPointFoundationRsDto:
        return TerritoryPointFoundationRsDto(**asdict(dc))

    @staticmethod
    def to_point_water_rs_dto(dc: WaterDC) -> TerritoryPointWaterRsDto:
        return TerritoryPointWaterRsDto(**asdict(dc))

    @staticmethod
    def to_point_climate_rs_dto(dc: ClimateDC) -> TerritoryPointClimateRsDto:
        return TerritoryPointClimateRsDto(**asdict(dc))