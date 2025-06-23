from pydantic import BaseModel
from typing import Optional

class GroundInBD(BaseModel):
    ground_name: str
    ground_description: str
    ground_density: Optional[float] = None
    ground_humidity: Optional[float] = None
    ground_hardness_Moos: Optional[int] = None
    ground_picture: Optional[str] = None

class GroundPicture(BaseModel):
    ground_id: int
    ground_picture: str