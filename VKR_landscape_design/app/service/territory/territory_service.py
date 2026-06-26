from sqlalchemy.orm import Session

from app.components.climate.climate_component import ClimateComponent
from app.components.landscape.landscape_component import LandscapeComponent
from app.components.relief.relief_component import ReliefComponent
from app.components.soil.soil_component import SoilComponent
from app.components.territory.territory_component import TerritoryComponent
from app.service.territory.territory_dto import TerritoryPointSearchRsDto
from app.service.territory.territory_dto_mapper import TerritoryDtoMapper
from app.components.ground.ground_component import GroundComponent
from app.components.plant.plant_component import PlantComponent
from app.components.foundation.foundation_component import FoundationComponent
from app.components.water.water_component import WaterComponent

class TerritoryService:

    def __init__(self, db: Session):
        self.db = db
        self.landscape_component = LandscapeComponent(db)
        self.territory_component = TerritoryComponent(db)
        self.climate_component = ClimateComponent(db)
        self.relief_component = ReliefComponent(db)
        self.soil_component = SoilComponent(db)
        self.ground_component = GroundComponent(db)
        self.plant_component = PlantComponent(db)
        self.foundation_component = FoundationComponent(db)
        self.water_component = WaterComponent(db)

    def get_territory_by_point(self, point_x: float, point_y: float) -> TerritoryPointSearchRsDto | None:

        territory = self.territory_component.get_by_point(point_x=point_x,point_y=point_y)
        if territory is None:
            return None
        landscape = self.landscape_component.get_by_id(territory.landscape_id)

        climates = []
        reliefs = []
        soils = []
        grounds = []
        plants = []
        foundations = []
        waters = []

        if landscape is not None:
            climates = self.climate_component.get_all_by_landscape_id(landscape.id) or []
            reliefs = self.relief_component.get_all_by_landscape_id(landscape.id) or []
            soils = self.soil_component.get_all_by_landscape_id(landscape.id) or []
            grounds = self.ground_component.get_all_by_landscape_id(landscape.id) or []
            plants = self.plant_component.get_all_by_landscape_id(landscape.id) or []
            foundations = self.foundation_component.get_all_by_landscape_id(landscape.id) or []
            waters = self.water_component.get_all_by_landscape_id(landscape.id) or []

        return TerritoryDtoMapper.to_point_search_rs_dto(
            territory=territory,
            landscape=landscape,
            soils=soils,
            grounds=grounds,
            plants=plants,
            reliefs=reliefs,
            foundations=foundations,
            waters=waters,
            climates=climates,
        )