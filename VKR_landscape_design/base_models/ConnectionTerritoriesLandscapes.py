from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesLandscapesInBD(BaseModel):
    territorie_id: int
    landscape_id: int