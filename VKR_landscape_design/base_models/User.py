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
    user_isFemale: Optional[int] = None
    user_picture: Optional[str] = None
    user_isAdmin: int

class UserRegister(BaseModel):
    user_login: str
    user_password: str
    user_email: str

class UserAuthorization(BaseModel):
    user_login: str
    user_password: str

class UserPicture(BaseModel):
    user_id: int
    user_picture: str
