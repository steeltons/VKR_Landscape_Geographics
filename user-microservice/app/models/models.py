import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Boolean, Integer, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .entity_mixin import EntityMixin
from db.database import Base

class FileMetadata(Base, EntityMixin):
    __tablename__ = 'file_metadata'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key= True, default= uuid.uuid4)

    name: Mapped[str] = mapped_column(String, nullable=False)
    file_group: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str] = mapped_column(String, nullable=False)

class User(Base, EntityMixin):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default= uuid.uuid4)

    login: Mapped[str] = mapped_column(String, nullable=False, unique= True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique= True)

class UserProfile(Base, EntityMixin):
    __tablename__ = 'user_profiles'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

class UserPassword(Base, EntityMixin):
    __tablename__ = 'user_passwords'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default= uuid.uuid4)

    password: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

class UserAuthority(Base, EntityMixin):
    __tablename__ = 'user_authorities'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    authority : Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False
    )

class AuthRefreshSession(Base):
    __tablename__ = 'auth_refresh_sessions'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    token_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable= False, unique= True, default= uuid.uuid4)

    refresh_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone= True), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    replaced_by_token_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth_refresh_sessions.token_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )




