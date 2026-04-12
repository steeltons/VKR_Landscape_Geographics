import hashlib
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import AuthRefreshSession

def _hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

def create_session(db: Session, user_id: uuid.UUID, token_id: uuid.UUID, raw_refresh_token: str, expires_at: datetime) -> AuthRefreshSession:
    token_hash = hashlib.sha256(raw_refresh_token.encode("utf-8")).hexdigest()

    session = AuthRefreshSession(
        user_id=user_id,
        token_id=token_id,
        refresh_token_hash=token_hash,
        issued_at=datetime.now(timezone.utc),
        expires_at=expires_at,
        revoked_at=None,
        replaced_by_token_id=None,
    )

    db.add(session)
    db.flush()
    return session

def get_valid_session_by_refresh_token(db: Session, raw_refresh_token: str,) -> AuthRefreshSession | None:
    token_hash = _hash_token(raw_refresh_token)

    return db.scalar(
        select(AuthRefreshSession).where(
            AuthRefreshSession.refresh_token_hash == token_hash,
            AuthRefreshSession.revoked_at.is_(None),
            AuthRefreshSession.expires_at > datetime.now(timezone.utc),
        )
    )


def rotate_session(db: Session, current_session: AuthRefreshSession, new_token_id: uuid.UUID, new_raw_refresh_token: str, new_expires_at) -> AuthRefreshSession:
    new_session = create_session(db= db, user_id= current_session.user_id, token_id= new_token_id, raw_refresh_token= new_raw_refresh_token, expires_at= new_expires_at)

    current_session.revoked_at = datetime.now(timezone.utc)
    current_session.replaced_by_token_id = new_token_id

    db.flush()
    return new_session

def revoke_session_by_refresh_token(db: Session, raw_refresh_token: str) -> None:
    token_hash = _hash_token(raw_refresh_token)

    session = db.scalar(
        select(AuthRefreshSession).where(
            AuthRefreshSession.refresh_token_hash == token_hash,
            AuthRefreshSession.revoked_at.is_(None),
        )
    )

    if session is None:
        return

    session.revoked_at = datetime.now(timezone.utc)
    db.flush()