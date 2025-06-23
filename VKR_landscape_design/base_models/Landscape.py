from pydantic import BaseModel
from typing import Optional

class LandscapeInBD(BaseModel):
   landscape_name: str
   landscape_description: str
   landscape_picture: Optional[str] = None

class LandscapePicture(BaseModel):
   landscape_id: int
   landscape_picture: str