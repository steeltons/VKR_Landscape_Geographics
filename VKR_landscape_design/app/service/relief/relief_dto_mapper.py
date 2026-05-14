from app.components.relief.relief_dc import ReliefDC
from app.service.relief.relief_dto import ReliefRsDto


class ReliefDtoMapper:
    @staticmethod
    def to_rs_dto(dc: ReliefDC) -> ReliefRsDto:
        return ReliefRsDto(
            id= dc.id,
            name= dc.name,
            description= dc.description,
            picture_id= dc.picture_id,
        )

    @staticmethod
    def to_list_rs_dto(items: list[ReliefDC]) -> list[ReliefRsDto]:
        return [ReliefDtoMapper.to_rs_dto(item) for item in items]