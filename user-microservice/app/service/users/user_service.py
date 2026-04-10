from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import User
from app.service.users.dto.user_dto import UserRsDto


def get_all_users(db: Session) -> list[UserRsDto]:
    users = db.scalars(select(User)).all()

    return [UserRsDto.model_validate(user) for user in users]