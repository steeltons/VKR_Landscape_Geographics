from pydantic import BaseModel
from typing import Optional


class ClimatInBD(BaseModel):
   climat_name: str
   climat_description: Optional[str] = None
   climat_picture: Optional[int] = None


class ClimatPicture(BaseModel):
   climat_id: int
   climat_picture_id: int