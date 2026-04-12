from uuid import UUID
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session

from app.models.models import User, UserAuthorityType, UserAuthority, UserProfile
from app.service.users.dto.user_dto import UserRsDto, AddUserRqDto, UserAuthoritiesRqDto, FullyCreateUserRqDto


def get_all_users(db: Session) -> list[UserRsDto]:
    users = db.scalars(select(User)).all()

    return [UserRsDto.model_validate(user) for user in users]

def get_by_email(email: str, db: Session) -> UserRsDto | None:
    user = (db.query(User)
            .filter(User.email == email)
            .first())

    if user:
        return UserRsDto.model_validate(user)
    else:
        return None

def add_user(user_authorities: list[UserAuthorityType], body: AddUserRqDto, db: Session) -> UserRsDto:
    if UserAuthorityType.ADD_USERS not in user_authorities:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    user = User(login= body.login, email= body.email, is_active= True)

    db.add(user)
    db.flush()
    __add_user_password(body.password, user, db)

    return UserRsDto.model_validate(user)

def grant_authorities(user_id: UUID, caller_authorities: list[UserAuthorityType], body: UserAuthoritiesRqDto, db: Session) -> None:
    if UserAuthorityType.GRANT_PERMISSIONS not in caller_authorities:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    requested_authorities = set(body.authorities)

    if not requested_authorities:
        return

    existing_authorities_rows = (
        db.query(UserAuthority.authority)
        .filter(
            (UserAuthority.user_id == user_id)
            & (UserAuthority.is_active.is_(True))
            & (UserAuthority.authority.in_(requested_authorities))
        )
        .all()
    )

    existing_authorities = {row[0] for row in existing_authorities_rows}
    missing_authorities = requested_authorities - existing_authorities

    new_authorities = [UserAuthority(user_id=user_id, authority=authority) for authority in missing_authorities]

    db.add_all(new_authorities)
    db.commit()

def revoke_authorities(user_id: UUID, caller_authorities: list[UserAuthorityType], body: UserAuthoritiesRqDto, db: Session) -> None:
    if UserAuthorityType.REVOKE_PERMISSIONS not in caller_authorities:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    if not body.authorities:
        return

    stmt = (
        update(UserAuthority)
        .where(
            (UserAuthority.user_id == user_id)
            & (UserAuthority.is_active.is_(True))
            & (UserAuthority.authority.in_(body.authorities)),
        )
        .values(
            is_active=False,
            updated_at= datetime.now(timezone.utc),
        )
    )

    db.execute(stmt)
    db.commit()

def add_full_user(body: FullyCreateUserRqDto, db: Session) -> UserRsDto:
    main_user = User(login= body.login, email= body.email, is_active= True)
    db.add(main_user)
    db.flush()

    user_profile = UserProfile(first_name= body.first_name, middle_name= body.middle_name, last_name= body.last_name, gender= body.gender, age= body.age, user_id= main_user.id)
    db.add(user_profile)
    db.flush()

    __add_user_password(body.password, main_user, db)

    return UserRsDto.model_validate(main_user)

def get_by_login(login: str, db: Session) -> UserRsDto | None:
    user = (db.query(User)
            .filter(User.login == login)
            .first())

    if user:
        return UserRsDto.model_validate(user)
    else:
        return None

def __add_user_password(user_password: str, user: User, db: Session) -> None:
    db.execute(
        text("""
            INSERT INTO user_passwords(id, password, user_id, created_at, updated_at, is_active)
            VALUES(
                gen_random_uuid(),
                crypt(:password, gen_salt('bf', 12)),
                :user_id,
                NOW(),
                NOW(),
                true
                )
        """),
        {'password' : user_password, 'user_id' : user.id}
    )
    db.commit()
    db.refresh(user)