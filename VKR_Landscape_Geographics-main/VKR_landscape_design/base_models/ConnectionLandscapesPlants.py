from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesPlantsInBD(BaseModel):
    landscape_id: int
    plant_id: int