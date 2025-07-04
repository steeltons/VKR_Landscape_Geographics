from pydantic import BaseModel
from typing import Optional

class SoilInBD(BaseModel):
    soil_name: str
    soil_description: Optional[str] = None
    soil_acidity: Optional[float] = None
    soil_minerals: Optional[str] = None
    soil_profile: Optional[str] = None
    soil_picture: Optional[int] = None

class SoilPicture(BaseModel):
    soil_id: int
    soil_picture_id: int