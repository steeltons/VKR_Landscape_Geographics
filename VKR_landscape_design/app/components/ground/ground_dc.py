from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GroundDC:
    id: int
    name: str
    description: str | None
    density: Decimal | None
    humidity: Decimal | None
    solidity: Decimal | None
    picture_id: UUID | None
    is_active: bool