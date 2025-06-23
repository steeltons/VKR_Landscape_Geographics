from pydantic import BaseModel
from typing import Optional

class ClimatInBD(BaseModel):
   climat_name: str
   climat_description: str