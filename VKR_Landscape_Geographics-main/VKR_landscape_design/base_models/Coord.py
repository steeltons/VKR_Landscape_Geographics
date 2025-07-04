from pydantic import BaseModel
from typing import Optional

class CoordInBD(BaseModel):
    coords_coord_x: float
    coords_coord_y: float
    coords_territorie_id: int
    coords_order: int