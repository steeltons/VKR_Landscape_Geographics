from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesWatersInBD(BaseModel):
    landscape_id: int
    water_id: int