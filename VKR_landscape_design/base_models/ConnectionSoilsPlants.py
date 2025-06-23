from pydantic import BaseModel
from typing import Optional

class ConnectionSoilsPlantsInBD(BaseModel):
    soil_id: int
    plant_id: int