from app.components.foundation.foundation_dc import FoundationDC
from app.service.foundation.foundation_dto import FoundationRsDto, FoundationsRsDto


class FoundationDtoMapper:
    @staticmethod
    def to_rs_dto(dc: FoundationDC) -> FoundationRsDto:
        return FoundationRsDto(**dc.__dict__)

    @staticmethod
    def to_list_rs_dto(
        items: list[FoundationDC],
        *,
        limit: int,
        offset: int,
    ) -> FoundationsRsDto:
        return FoundationsRsDto(
            items=[FoundationDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )