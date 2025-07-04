from pydantic import BaseModel
from typing import Optional

class LandscapeInBD(BaseModel):
   landscape_name: str
   landscape_code: Optional[str] = None
   landscape_description: Optional[str] = None
   landscape_area_in_square_kilometers: Optional[float] = None
   landscape_area_in_percents: Optional[float] = None
   landscape_KR: Optional[float] = None
   landscape_picture: Optional[int] = None


class LandscapePicture(BaseModel):
   landscape_id: int
   landscape_picture_id: int