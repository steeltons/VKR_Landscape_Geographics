from pydantic import BaseModel, ConfigDict


class TerritoryCreateParamsRqDto(BaseModel):
    description: str | None = None
    landscape_id: int | None = None


class TerritoryUpdateParamsRqDto(BaseModel):
    description: str | None = None
    landscape_id: int | None = None


class TerritoryRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None
    landscape_id: int | None
    is_active: bool


class TerritoriesRsDto(BaseModel):
    items: list[TerritoryRsDto]
    limit: int
    offset: int