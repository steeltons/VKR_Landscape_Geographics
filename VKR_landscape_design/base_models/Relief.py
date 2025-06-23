from pydantic import BaseModel
from typing import Optional

class ReliefInBD(BaseModel):
   relief_name: str
   relief_description: str
   relief_picture: Optional[str] = None

class ReliefPicture(BaseModel):
   relief_id: int
   relief_picture: str