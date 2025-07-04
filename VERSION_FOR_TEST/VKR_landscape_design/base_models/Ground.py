from pydantic import BaseModel
from typing import Optional

class GroundInBD(BaseModel):
    ground_name: str
    ground_description: Optional[str] = None
    ground_density: Optional[float] = None
    ground_humidity: Optional[float] = None
    ground_solidity: Optional[float] = None
    ground_picture: Optional[int] = None

class GroundPicture(BaseModel):
    ground_id: int
    ground_picture_id: int