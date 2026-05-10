from app.components.ground.ground_dc import GroundDC
from app.service.ground.ground_dto import GroundRsDto, GroundsRsDto


class GroundDtoMapper:
    @staticmethod
    def to_rs_dto(dc: GroundDC) -> GroundRsDto:
        return GroundRsDto(
            id=dc.id,
            name=dc.name,
            description=dc.description,
            density=dc.density,
            humidity=dc.humidity,
            solidity=dc.solidity,
            picture_id=dc.picture_id,
            is_active=dc.is_active,
        )

    @staticmethod
    def to_list_rs_dto(
        items: list[GroundDC],
        *,
        limit: int,
        offset: int,
    ) -> GroundsRsDto:
        return GroundsRsDto(
            items=[GroundDtoMapper.to_rs_dto(item) for item in items],
            limit=limit,
            offset=offset,
        )