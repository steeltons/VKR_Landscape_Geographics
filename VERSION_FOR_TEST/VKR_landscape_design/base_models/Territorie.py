from pydantic import BaseModel
from typing import Optional

class TerritorieInBD(BaseModel):
    territorie_landscape_id: Optional[int] = None
    territorie_desciption: Optional[str] = None
    territorie_color_r: Optional[int] = None
    territorie_color_g: Optional[int] = None
    territorie_color_b: Optional[int] = None