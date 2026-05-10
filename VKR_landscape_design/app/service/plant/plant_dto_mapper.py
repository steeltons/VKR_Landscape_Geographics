from app.components.plant.plant_dc import PlantDC
from app.service.plant.plant_dto import PlantRsDto, PlantsRsDto


class PlantDtoMapper:
    @staticmethod
    def to_rs_dto(dc: PlantDC) -> PlantRsDto:
        return PlantRsDto(
            id=dc.id,
            name=dc.name,
            description=dc.description,
            picture_id=dc.picture_id,
            is_active=dc.is_active,
        )

    @staticmethod
    def to_list_rs_dto(
        items: list[PlantDC],
        *,
        limit: int,
        offset: int,
    ) -> PlantsRsDto:
        return PlantsRsDto(
            items=[PlantDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )