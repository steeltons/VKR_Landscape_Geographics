from pydantic import BaseModel
from typing import Optional

class PictureInBD(BaseModel):
    picture_base64: str
