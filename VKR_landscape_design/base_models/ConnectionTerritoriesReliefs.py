from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesReliefsInBD(BaseModel):
    territorie_id: int
    relief_id: int