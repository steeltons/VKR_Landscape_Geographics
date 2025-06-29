from pydantic import BaseModel
from typing import Optional

class TerritorieInBD(BaseModel):
    territorie_landscape_id: Optional[int] = None
    territorie_desciption: Optional[str] = None