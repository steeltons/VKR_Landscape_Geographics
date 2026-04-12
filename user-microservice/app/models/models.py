import uuid
import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, BigInteger, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.entity_mixin import EntityMixin
from app.db.database import Base

class UserAuthorityType(enum.Enum):

    ADD_USERS = ("ADD_USERS", "Добавление пользователей")
    REMOVE_USERS = ("REMOVE_USERS", "Удаление пользователей")
    EDIT_USERS = ("EDIT_USERS", "Редактирование пользователей")
    GRANT_PERMISSIONS = ('GRANT_PERMISSIONS', 'Выдача прав')
    REVOKE_PERMISSIONS = ('REVOKE_PERMISSIONS', 'Отзыв прав')

    def __new__(cls, system_name: str, display_name: str):
        obj = object.__new__(cls)
        obj._value_ = system_name
        obj.system_name = system_name
        obj.display_name = display_name
        return obj

    @classmethod
    def from_system_name(cls, code: str) -> "UserAuthorityType":
        for item in cls:
            if item.system_name == code:
                return item
        raise ValueError(f"Unknown authority code: {code}")

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

    authority: Mapped[UserAuthorityType] = mapped_column(
        Enum(
            UserAuthorityType,
            name= "authority",
            native_enum= False,
            validate_strings= True,
            values_callable= lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
    )

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
