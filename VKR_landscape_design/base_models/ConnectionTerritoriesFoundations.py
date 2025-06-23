from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesFoundationsInBD(BaseModel):
    territorie_id: int
    foundation_id: int