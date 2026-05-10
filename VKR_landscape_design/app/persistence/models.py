import uuid
from decimal import Decimal

from geoalchemy2 import Geometry
from sqlalchemy import (BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.entity_mixin import EntityMixin
from app.configs.db.database import Base

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

    landscape_links: Mapped[list["LandscapeSoilConnection"]] = relationship(
        back_populates="soil",
        cascade="all, delete-orphan",
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

    soil_links: Mapped[list["LandscapeSoilConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    ground_links: Mapped[list["LandscapeGroundConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    plant_links: Mapped[list["LandscapePlantConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    relief_links: Mapped[list["LandscapeReliefConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    foundation_links: Mapped[list["LandscapeFoundationConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    water_links: Mapped[list["LandscapeWaterConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    climate_links: Mapped[list["LandscapeClimateConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
    )
    territory_links: Mapped[list["TerritoryLandscapeConnection"]] = relationship(
        back_populates="landscape",
        cascade="all, delete-orphan",
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

    landscape_links: Mapped[list["LandscapeGroundConnection"]] = relationship(
        back_populates="ground",
        cascade="all, delete-orphan",
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

    landscape_links: Mapped[list["LandscapePlantConnection"]] = relationship(
        back_populates="plant",
        cascade="all, delete-orphan",
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

    landscape_links: Mapped[list["LandscapeReliefConnection"]] = relationship(
        back_populates="relief",
        cascade="all, delete-orphan",
    )


class Foundation(Base, EntityMixin):
    __tablename__ = "foundations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    roof_root_depth: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)

    picture_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("file_metadata.id"),
        nullable=True,
    )

    landscape_links: Mapped[list["LandscapeFoundationConnection"]] = relationship(
        back_populates="foundation",
        cascade="all, delete-orphan",
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

    landscape_links: Mapped[list["LandscapeWaterConnection"]] = relationship(
        back_populates="water",
        cascade="all, delete-orphan",
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

    landscape_links: Mapped[list["LandscapeClimateConnection"]] = relationship(
        back_populates="climate",
        cascade="all, delete-orphan",
    )


class Territory(Base, EntityMixin):
    __tablename__ = "territories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Оставлено для обратной совместимости с текущей миграцией.
    # Новая онтологическая связь territory <-> landscape задаётся через
    # TerritoryLandscapeConnection, потому что территория может включать
    # несколько ландшафтов.
    landscape_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("landscapes.id"),
        nullable=True,
    )

    landscape_links: Mapped[list["TerritoryLandscapeConnection"]] = relationship(
        back_populates="territory",
        cascade="all, delete-orphan",
    )
    geometries: Mapped[list["TerritoryGeometry"]] = relationship(
        back_populates="territory",
        cascade="all, delete-orphan",
    )


class TerritoryGeometry(Base):
    __tablename__ = "territory_geometries"

    geometry_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    territory_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("territories.id", ondelete="CASCADE"),
        nullable=False,
    )

    geom: Mapped[object] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    territory: Mapped["Territory"] = relationship(back_populates="geometries")

    __table_args__ = (
        Index("ix_territory_geometries_territory_id", "territory_id"),
        Index("ix_territory_geometries_geom", "geom", postgresql_using="gist"),
    )


class OntologyConnectionMixin:
    """
    Общие поля для онтологических связей.

    relation_type:
        Семантика связи: typical, dominant, possible, limiting, forbidden и т.п.

    role:
        Роль связанного объекта внутри ландшафта/территории:
        main, secondary, accompanying, rare и т.п.

    weight:
        Сила/значимость связи. Можно использовать для ранжирования и ML.
        Рекомендуемый диапазон: 0..1.

    confidence:
        Достоверность знания. Отличается от weight:
        weight = насколько объект характерен;
        confidence = насколько мы уверены в этом утверждении.

    source:
        Источник знания: эксперт, справочник, импорт, расчёт, модель.

    properties:
        Контекстные свойства связи. Например:
        {"season": "summer", "note": "...", "soil_share": 0.62}
    """

    relation_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default=text("'typical'"),
    )
    role: Mapped[str | None] = mapped_column(String, nullable=True)
    weight: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    properties: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class LandscapeSoilConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_soils"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    soil_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("soils.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="soil_links")
    soil: Mapped["Soil"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "soil_id", "relation_type", name="uq_landscape_soil_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_cls_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_cls_confidence_range"),
    )


class LandscapeGroundConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_grounds"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    ground_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("grounds.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="ground_links")
    ground: Mapped["Ground"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "ground_id", "relation_type", name="uq_landscape_ground_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clg_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clg_confidence_range"),
    )


class LandscapePlantConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_plants"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    plant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("plants.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="plant_links")
    plant: Mapped["Plant"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "plant_id", "relation_type", name="uq_landscape_plant_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clp_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clp_confidence_range"),
    )


class LandscapeReliefConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_reliefs"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    relief_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("reliefs.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="relief_links")
    relief: Mapped["Relief"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "relief_id", "relation_type", name="uq_landscape_relief_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clr_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clr_confidence_range"),
    )


class LandscapeFoundationConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_foundations"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    foundation_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("foundations.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="foundation_links")
    foundation: Mapped["Foundation"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "foundation_id", "relation_type", name="uq_landscape_foundation_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clf_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clf_confidence_range"),
    )


class LandscapeWaterConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_waters"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    water_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("waters.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="water_links")
    water: Mapped["Water"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "water_id", "relation_type", name="uq_landscape_water_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clw_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clw_confidence_range"),
    )


class LandscapeClimateConnection(Base, OntologyConnectionMixin):
    __tablename__ = "connections_landscapes_climates"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)
    climate_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("climates.id"), nullable=False)

    landscape: Mapped["Landscape"] = relationship(back_populates="climate_links")
    climate: Mapped["Climate"] = relationship(back_populates="landscape_links")

    __table_args__ = (
        UniqueConstraint("landscape_id", "climate_id", "relation_type", name="uq_landscape_climate_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_clc_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_clc_confidence_range"),
    )


class TerritoryLandscapeConnection(Base, OntologyConnectionMixin):
    """
    Связь территории и ландшафта.

    Нужна, чтобы не ограничивать территорию одним landscape_id.
    """

    __tablename__ = "connections_territories_landscapes"

    connection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    territory_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("territories.id"), nullable=False)
    landscape_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("landscapes.id"), nullable=False)

    territory: Mapped["Territory"] = relationship(back_populates="landscape_links")
    landscape: Mapped["Landscape"] = relationship(back_populates="territory_links")

    __table_args__ = (
        UniqueConstraint("territory_id", "landscape_id", "relation_type", name="uq_territory_landscape_relation"),
        CheckConstraint("weight IS NULL OR (weight >= 0 AND weight <= 1)", name="ck_ctl_weight_range"),
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_ctl_confidence_range"),
    )
