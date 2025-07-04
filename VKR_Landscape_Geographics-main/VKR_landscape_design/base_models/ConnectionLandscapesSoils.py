from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesSoilsInBD(BaseModel):
    landscape_id: int
    soil_id: int