import uuid

from sqlalchemy import String, ForeignKey, Boolean, Integer, BigInteger
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


