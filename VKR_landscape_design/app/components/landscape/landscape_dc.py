from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class LandscapeDC:
    id: int
    name: str
    code: str | None
    description: str | None
    area_square: Decimal | None
    area_percentage: Decimal | None
    kr: Decimal | None
    picture_id: UUID | None
    is_active: bool