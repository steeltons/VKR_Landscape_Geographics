from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.jwt_guard import require_access_token

from app.db.dependencies import get_db
from app.service.users.dto.user_dto import UserRsDto
from app.service.users.user_service import get_all_users, get_by_email, get_by_login

router = APIRouter(
    prefix= "/api/v1/users",
    tags= ["users"],
    dependencies= [Depends(require_access_token)]
)

@router.get("", response_model=list[UserRsDto])
def get_users(db: Session = Depends(get_db)) -> list[UserRsDto]:
    return get_all_users(db)

@router.get("/email/{email}", response_model=list[UserRsDto])
def get_user_by_email(email: str, db: Session = Depends(get_db)) -> UserRsDto:
    return get_by_email(email, db)

@router.get("/login/{login}", response_model=UserRsDto | None)
def get_user_by_login(login: str, db: Session = Depends(get_db)) -> UserRsDto | None:
    return get_by_login(login, db)