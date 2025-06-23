from pydantic import BaseModel
from typing import Optional

class WaterInBD(BaseModel):
   water_name: str
   water_description: str