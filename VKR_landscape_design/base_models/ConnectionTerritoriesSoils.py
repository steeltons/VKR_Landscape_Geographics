from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesSoilsInBD(BaseModel):
    territorie_id: int
    soil_id: int