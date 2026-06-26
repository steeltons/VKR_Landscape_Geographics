"""init_script

Revision ID: 2026_04_08_12_00_init_script
Revises: stey
Create Date: 2026-04-08 12:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2026_04_08_12_00_init_script"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "file_metadata",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file_group", sa.String(), nullable=False),
        sa.Column("mime_type", sa.String(), nullable=False),
        sa.Column("extension", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "soils",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("acidity", sa.Numeric(), nullable=True),
        sa.Column("minerals", sa.String(), nullable=True),
        sa.Column("profile", sa.String(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_soils_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "landscapes",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("area_square", sa.Numeric(), nullable=True),
        sa.Column("area_percentage", sa.Numeric(), nullable=True),
        sa.Column("kr", sa.Numeric(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_landscapes_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "grounds",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("density", sa.Numeric(), nullable=True),
        sa.Column("humidity", sa.Numeric(), nullable=True),
        sa.Column("solidity", sa.Numeric(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_grounds_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "plants",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_plants_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "reliefs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_reliefs_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "foundations",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("roof_root_depth", sa.Numeric(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_foundations_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "waters",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_waters_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "climates",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("picture_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["picture_id"],
            ["file_metadata.id"],
            name="fk_climates_picture_id_file_metadata",
        ),
    )

    op.create_table(
        "territories",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("landscape_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_territories_landscape_id_landscapes",
        ),
    )

    op.create_table(
        "connections_landscapes_soils",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("soil_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_cls_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["soil_id"],
            ["soils.id"],
            name="fk_cls_soil_id_soils",
        ),
    )

    op.create_table(
        "connections_landscapes_grounds",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("ground_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clg_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["ground_id"],
            ["grounds.id"],
            name="fk_clg_ground_id_grounds",
        ),
    )

    op.create_table(
        "connections_landscapes_plants",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("plant_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clp_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["plant_id"],
            ["plants.id"],
            name="fk_clp_plant_id_plants",
        ),
    )

    op.create_table(
        "connections_landscapes_reliefs",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("relief_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clr_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["relief_id"],
            ["reliefs.id"],
            name="fk_clr_relief_id_reliefs",
        ),
    )

    op.create_table(
        "connections_landscapes_foundations",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("foundation_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clf_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["foundation_id"],
            ["foundations.id"],
            name="fk_clf_foundation_id_foundations",
        ),
    )

    op.create_table(
        "connections_landscapes_waters",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("water_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clw_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["water_id"],
            ["waters.id"],
            name="fk_clw_water_id_waters",
        ),
    )

    op.create_table(
        "connections_landscapes_climates",
        sa.Column("connection_id", sa.BigInteger(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column("climate_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_clc_landscape_id_landscapes",
        ),
        sa.ForeignKeyConstraint(
            ["climate_id"],
            ["climates.id"],
            name="fk_clc_climate_id_climates",
        ),
    )

    op.create_index("ix_soils_picture_id", "soils", ["picture_id"])
    op.create_index("ix_landscapes_picture_id", "landscapes", ["picture_id"])
    op.create_index("ix_grounds_picture_id", "grounds", ["picture_id"])
    op.create_index("ix_plants_picture_id", "plants", ["picture_id"])
    op.create_index("ix_reliefs_picture_id", "reliefs", ["picture_id"])
    op.create_index("ix_foundations_picture_id", "foundations", ["picture_id"])
    op.create_index("ix_waters_picture_id", "waters", ["picture_id"])
    op.create_index("ix_climates_picture_id", "climates", ["picture_id"])
    op.create_index("ix_territories_landscape_id", "territories", ["landscape_id"])

    op.create_index("ix_cls_landscape_id", "connections_landscapes_soils", ["landscape_id"])
    op.create_index("ix_cls_soil_id", "connections_landscapes_soils", ["soil_id"])

    op.create_index("ix_clg_landscape_id", "connections_landscapes_grounds", ["landscape_id"])
    op.create_index("ix_clg_ground_id", "connections_landscapes_grounds", ["ground_id"])

    op.create_index("ix_clp_landscape_id", "connections_landscapes_plants", ["landscape_id"])
    op.create_index("ix_clp_plant_id", "connections_landscapes_plants", ["plant_id"])

    op.create_index("ix_clr_landscape_id", "connections_landscapes_reliefs", ["landscape_id"])
    op.create_index("ix_clr_relief_id", "connections_landscapes_reliefs", ["relief_id"])

    op.create_index("ix_clf_landscape_id", "connections_landscapes_foundations", ["landscape_id"])
    op.create_index("ix_clf_foundation_id", "connections_landscapes_foundations", ["foundation_id"])

    op.create_index("ix_clw_landscape_id", "connections_landscapes_waters", ["landscape_id"])
    op.create_index("ix_clw_water_id", "connections_landscapes_waters", ["water_id"])

    op.create_index("ix_clc_landscape_id", "connections_landscapes_climates", ["landscape_id"])
    op.create_index("ix_clc_climate_id", "connections_landscapes_climates", ["climate_id"])


def downgrade() -> None:
    op.drop_index("ix_clc_climate_id", table_name="connections_landscapes_climates")
    op.drop_index("ix_clc_landscape_id", table_name="connections_landscapes_climates")

    op.drop_index("ix_clw_water_id", table_name="connections_landscapes_waters")
    op.drop_index("ix_clw_landscape_id", table_name="connections_landscapes_waters")

    op.drop_index("ix_clf_foundation_id", table_name="connections_landscapes_foundations")
    op.drop_index("ix_clf_landscape_id", table_name="connections_landscapes_foundations")

    op.drop_index("ix_clr_relief_id", table_name="connections_landscapes_reliefs")
    op.drop_index("ix_clr_landscape_id", table_name="connections_landscapes_reliefs")

    op.drop_index("ix_clp_plant_id", table_name="connections_landscapes_plants")
    op.drop_index("ix_clp_landscape_id", table_name="connections_landscapes_plants")

    op.drop_index("ix_clg_ground_id", table_name="connections_landscapes_grounds")
    op.drop_index("ix_clg_landscape_id", table_name="connections_landscapes_grounds")

    op.drop_index("ix_cls_soil_id", table_name="connections_landscapes_soils")
    op.drop_index("ix_cls_landscape_id", table_name="connections_landscapes_soils")

    op.drop_index("ix_territories_landscape_id", table_name="territories")
    op.drop_index("ix_climates_picture_id", table_name="climates")
    op.drop_index("ix_waters_picture_id", table_name="waters")
    op.drop_index("ix_foundations_picture_id", table_name="foundations")
    op.drop_index("ix_reliefs_picture_id", table_name="reliefs")
    op.drop_index("ix_plants_picture_id", table_name="plants")
    op.drop_index("ix_grounds_picture_id", table_name="grounds")
    op.drop_index("ix_landscapes_picture_id", table_name="landscapes")
    op.drop_index("ix_soils_picture_id", table_name="soils")

    op.drop_table("connections_landscapes_climates")
    op.drop_table("connections_landscapes_waters")
    op.drop_table("connections_landscapes_foundations")
    op.drop_table("connections_landscapes_reliefs")
    op.drop_table("connections_landscapes_plants")
    op.drop_table("connections_landscapes_grounds")
    op.drop_table("connections_landscapes_soils")

    op.drop_table("territories")
    op.drop_table("climates")
    op.drop_table("waters")
    op.drop_table("foundations")
    op.drop_table("reliefs")
    op.drop_table("plants")
    op.drop_table("grounds")
    op.drop_table("landscapes")
    op.drop_table("soils")
    op.drop_table("file_metadata")
