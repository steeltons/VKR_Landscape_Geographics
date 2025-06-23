from pydantic import BaseModel
from typing import Optional

class FoundationInBD(BaseModel):
   foundation_name: str
   foundation_description: str
   foundation_picture: Optional[str] = None

class FoundationPicture(BaseModel):
   foundation_id: int
   foundation_picture: str