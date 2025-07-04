from pydantic import BaseModel
from typing import Optional


class WaterInBD(BaseModel):
   water_name: str
   water_description: Optional[str] = None
   water_picture: Optional[int] = None


class WaterPicture(BaseModel):
   water_id: int
   water_picture_id: int
