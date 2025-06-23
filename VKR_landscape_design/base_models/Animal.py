from pydantic import BaseModel
from typing import Optional

class AnimalInBD(BaseModel):
    animal_name: str
    animal_description: str
    animal_kingdom: Optional[str] = None
    animal_philum: Optional[str] = None
    animal_class: Optional[str] = None
    animal_order: Optional[str] = None
    animal_family: Optional[str] = None
    animal_genus: Optional[str] = None
    animal_species: Optional[str] = None
    animal_picture: Optional[str] = None

class AnimalPicture(BaseModel):
    animal_id: int
    animal_picture: str