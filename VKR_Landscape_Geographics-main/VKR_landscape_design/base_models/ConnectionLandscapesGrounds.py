from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesGroundsInBD(BaseModel):
    landscape_id: int
    ground_id: int