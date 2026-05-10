from app.components.relief.relief_dc import ReliefDC
from app.service.relief.relief_dto import ReliefRsDto, ReliefsRsDto


class ReliefDtoMapper:
    @staticmethod
    def to_rs_dto(dc: ReliefDC) -> ReliefRsDto:
        return ReliefRsDto(**dc.__dict__)

    @staticmethod
    def to_list_rs_dto(
        items: list[ReliefDC],
        *,
        limit: int,
        offset: int,
    ) -> ReliefsRsDto:
        return ReliefsRsDto(
            items=[ReliefDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )