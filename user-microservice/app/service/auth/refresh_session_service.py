import hashlib
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.models import AuthRefreshSession


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
