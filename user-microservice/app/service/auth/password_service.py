import uuid

from sqlalchemy import text, select
from sqlalchemy.orm import Session

from app.service.auth.dto.auth_dto import AuthPrincipalDto
from app.models.models import User


def authenticate(db: Session, login: str, password: str) -> AuthPrincipalDto | None:
    query = text("""
                 SELECT u.id,
                        u.login,
                        u.email
                 FROM users u
                          JOIN user_passwords up ON up.user_id = u.id
                 WHERE u.login = :login
                   AND up.password = crypt(:password, up.password) LIMIT 1
                 """)

    row = db.execute(
        query,
        {
            "login": login,
            "password": password,
        },
    ).mappings().first()

    if row is None:
        return None

    return AuthPrincipalDto(
        user_id=row["id"],
        login=row["login"],
        email=row["email"],
    )

def get_principal_by_user_id(db: Session, user_id: uuid.UUID) -> AuthPrincipalDto | None:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    return AuthPrincipalDto(
        user_id= user.id,
        login= user.login,
        email= user.email,
    )