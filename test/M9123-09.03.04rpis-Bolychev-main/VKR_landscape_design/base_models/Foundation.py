from pydantic import BaseModel
from typing import Optional


class FoundationInBD(BaseModel):
   foundation_name: str
   foundation_description: Optional[str] = None
   foundation_depth_roof_root_in_meters: Optional[float] = None
   foundation_picture: Optional[int] = None


class FoundationPicture(BaseModel):
   foundation_id: int
   foundation_picture_id: int