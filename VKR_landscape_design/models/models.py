import uuid
from decimal import Decimal

from sqlalchemy import String, BigInteger, Text, ForeignKey, Numeric
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

class Soil(Base, EntityMixin):
    __tablename__ = "soils"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    acidity: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    minerals: Mapped[str | None] = mapped_column(String, nullable=True)
    profile: Mapped[str | None] = mapped_column(String, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )


class Landscape(Base, EntityMixin):
    __tablename__ = "landscapes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    area_square: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    area_percentage: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    kr: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )


class Ground(Base, EntityMixin):
    __tablename__ = "grounds"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    density: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    humidity: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    solidity: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )


class Plant(Base, EntityMixin):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )


class Relief(Base, EntityMixin):
    __tablename__ = "reliefs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

class Foundation(Base, EntityMixin):
    __tablename__ = "foundations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    roof_root_depth: Mapped[Decimal | None] = mapped_column(Numeric)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

class Water(Base, EntityMixin):
    __tablename__ = "waters"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

class Climate(Base, EntityMixin):
    __tablename__ = "climates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

class Territory(Base, EntityMixin):
    __tablename__ = "territories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    landscape_id: Mapped[BigInteger | None] = mapped_column(
        BigInteger,
        ForeignKey("landscapes.id"),
        nullable=True,
    )