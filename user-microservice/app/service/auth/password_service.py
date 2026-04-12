import uuid

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.service.auth.dto.auth_dto import AuthPrincipalDto


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