from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesReliefsInBD(BaseModel):
    landscape_id: int
    relief_id: int