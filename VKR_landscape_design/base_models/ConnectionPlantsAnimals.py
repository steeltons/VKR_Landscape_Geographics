from pydantic import BaseModel
from typing import Optional

class ConnectionPlantsAnimalsInBD(BaseModel):
    plant_id: int
    animal_id: int