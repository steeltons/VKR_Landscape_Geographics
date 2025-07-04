from pydantic import BaseModel
from typing import Optional

class ConnectionLandscapesFoundationsInBD(BaseModel):
    landscape_id: int
    foundation_id: int