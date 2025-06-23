from pydantic import BaseModel
from typing import Optional

class ConnectionTerritoriesClimatsInBD(BaseModel):
    territorie_id: int
    climat_id: int