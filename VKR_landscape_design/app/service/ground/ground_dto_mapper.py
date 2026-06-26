from app.components.ground.ground_dc import GroundDC
from app.service.ground.ground_dto import GroundRsDto


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
        )

    @staticmethod
    def to_list_rs_dto(items: list[GroundDC]) -> list[GroundRsDto]:
        return [GroundDtoMapper.to_rs_dto(item) for item in items]