from pydantic import BaseModel
from typing import Optional

class PlantInBD(BaseModel):
    plant_name: str
    plant_description: Optional[str] = None
    plant_picture: Optional[int] = None

class PlantPicture(BaseModel):
    plant_id: int
    plant_picture_id: int