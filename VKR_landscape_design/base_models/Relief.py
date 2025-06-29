from pydantic import BaseModel
from typing import Optional


class ReliefInBD(BaseModel):
   relief_name: str
   relief_description: Optional[str] = None
   relief_picture: Optional[int] = None


class ReliefPicture(BaseModel):
   relief_id: int
   relief_picture_id: int