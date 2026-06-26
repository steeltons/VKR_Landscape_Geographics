from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TerritoryDC:
    id: int
    description: str | None
    landscape_id: int | None
    is_active: bool