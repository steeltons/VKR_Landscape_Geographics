from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesClimatsInBD(BaseModel):
    landscape_id: int
    climat_id: int