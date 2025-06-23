from pydantic import BaseModel
from typing import Optional

class ConnectionSoilsGroundsInBD(BaseModel):
    soil_id: int
    ground_id: int