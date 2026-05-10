from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class FoundationDC:
    id: int
    name: str
    description: str | None
    roof_root_depth: Decimal | None
    picture_id: UUID | None
    is_active: bool