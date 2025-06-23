from pydantic import BaseModel
from typing import Optional

class TerritorieInBD(BaseModel):
    territorie_coord_x: float
    territorie_coord_y: float
    territorie_address: str