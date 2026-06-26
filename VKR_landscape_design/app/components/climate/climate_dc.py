from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ClimateDC:
    id: int
    name: str
    description: str | None
    picture_id: UUID | None
    is_active: bool