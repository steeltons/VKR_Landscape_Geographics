from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesWatersInBD(BaseModel):
    territorie_id: int
    water_id: int