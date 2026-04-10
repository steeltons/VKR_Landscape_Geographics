from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.service.users.dto.user_dto import UserRsDto
from app.service.users.user_service import get_all_users

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

@router.get("", response_model=list[UserRsDto])
def get_users(db: Session = Depends(get_db)) -> list[UserRsDto]:
    return get_all_users(db)