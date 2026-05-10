from app.components.territory.territory_dc import TerritoryDC
from app.persistence.models import Territory


class TerritoryComponentMapper:
    @staticmethod
    def to_dc(entity: Territory) -> TerritoryDC:
        return TerritoryDC(
            id=entity.id,
            description=entity.description,
            landscape_id=entity.landscape_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_dc_list(entities: list[Territory]) -> list[TerritoryDC]:
        return [TerritoryComponentMapper.to_dc(entity) for entity in entities]