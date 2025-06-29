from pydantic import BaseModel
from typing import Optional

class UserInBD(BaseModel):
    user_login: str
    user_password: str
    user_email: str
    user_surname: Optional[str] = None
    user_name: Optional[str] = None
    user_fathername: Optional[str] = None
    user_age: Optional[int] = None
    user_is_female: Optional[int] = None
    user_is_admin: Optional[str] = None
    user_picture: Optional[int] = None

class UserPicture(BaseModel):
    user_id: int
    user_picture_id: int

