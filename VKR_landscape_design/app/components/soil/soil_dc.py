from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SoilDC:
    id: int
    name: str
    description: str | None
    acidity: Decimal | None
    minerals: str | None
    profile: str | None
    picture_id: UUID | None
    is_active: bool