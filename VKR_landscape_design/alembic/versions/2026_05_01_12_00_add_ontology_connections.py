"""add ontology metadata to landscape connections

Revision ID: 2026_04_08_18_00_ontology_connections
Revises: 20260408_1500_geometries
Create Date: 2026-04-08 18:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "20260408_1800_onto"
down_revision = "20260408_1500_geometries"
branch_labels = None
depends_on = None


ONTOLOGY_COLUMNS = (
    sa.Column(
        "relation_type",
        sa.String(),
        nullable=False,
        server_default=sa.text("'typical'"),
    ),
    sa.Column("role", sa.String(), nullable=True),
    sa.Column("weight", sa.Numeric(5, 4), nullable=True),
    sa.Column("confidence", sa.Numeric(5, 4), nullable=True),
    sa.Column("source", sa.String(), nullable=True),
    sa.Column("comment", sa.Text(), nullable=True),
    sa.Column("properties", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
)


CONNECTION_TABLES = (
    {
        "table": "connections_landscapes_soils",
        "short": "cls",
        "left": "landscape_id",
        "right": "soil_id",
        "unique": "uq_landscape_soil_relation",
    },
    {
        "table": "connections_landscapes_grounds",
        "short": "clg",
        "left": "landscape_id",
        "right": "ground_id",
        "unique": "uq_landscape_ground_relation",
    },
    {
        "table": "connections_landscapes_plants",
        "short": "clp",
        "left": "landscape_id",
        "right": "plant_id",
        "unique": "uq_landscape_plant_relation",
    },
    {
        "table": "connections_landscapes_reliefs",
        "short": "clr",
        "left": "landscape_id",
        "right": "relief_id",
        "unique": "uq_landscape_relief_relation",
    },
    {
        "table": "connections_landscapes_foundations",
        "short": "clf",
        "left": "landscape_id",
        "right": "foundation_id",
        "unique": "uq_landscape_foundation_relation",
    },
    {
        "table": "connections_landscapes_waters",
        "short": "clw",
        "left": "landscape_id",
        "right": "water_id",
        "unique": "uq_landscape_water_relation",
    },
    {
        "table": "connections_landscapes_climates",
        "short": "clc",
        "left": "landscape_id",
        "right": "climate_id",
        "unique": "uq_landscape_climate_relation",
    },
)


def _add_ontology_columns(table_name: str) -> None:
    for column in ONTOLOGY_COLUMNS:
        op.add_column(table_name, column.copy())


def _drop_ontology_columns(table_name: str) -> None:
    for column_name in (
        "properties",
        "comment",
        "source",
        "confidence",
        "weight",
        "role",
        "relation_type",
    ):
        op.drop_column(table_name, column_name)


def _add_ontology_constraints(
    table_name: str,
    short_name: str,
    left_column: str,
    right_column: str,
    unique_name: str,
) -> None:
    op.create_unique_constraint(
        unique_name,
        table_name,
        [left_column, right_column, "relation_type"],
    )
    op.create_check_constraint(
        f"ck_{short_name}_weight_range",
        table_name,
        "weight IS NULL OR (weight >= 0 AND weight <= 1)",
    )
    op.create_check_constraint(
        f"ck_{short_name}_confidence_range",
        table_name,
        "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
    )
    op.create_index(
        f"ix_{short_name}_relation_type",
        table_name,
        ["relation_type"],
    )


def _drop_ontology_constraints(
    table_name: str,
    short_name: str,
    unique_name: str,
) -> None:
    op.drop_index(f"ix_{short_name}_relation_type", table_name=table_name)
    op.drop_constraint(f"ck_{short_name}_confidence_range", table_name, type_="check")
    op.drop_constraint(f"ck_{short_name}_weight_range", table_name, type_="check")
    op.drop_constraint(unique_name, table_name, type_="unique")


def upgrade() -> None:
    for table_meta in CONNECTION_TABLES:
        _add_ontology_columns(table_meta["table"])

    for table_meta in CONNECTION_TABLES:
        _add_ontology_constraints(
            table_name=table_meta["table"],
            short_name=table_meta["short"],
            left_column=table_meta["left"],
            right_column=table_meta["right"],
            unique_name=table_meta["unique"],
        )

    op.create_table(
        "connections_territories_landscapes",
        sa.Column(
            "connection_id",
            sa.BigInteger(),
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("territory_id", sa.BigInteger(), nullable=False),
        sa.Column("landscape_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "relation_type",
            sa.String(),
            nullable=False,
            server_default=sa.text("'typical'"),
        ),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("weight", sa.Numeric(5, 4), nullable=True),
        sa.Column("confidence", sa.Numeric(5, 4), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("properties", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(
            ["territory_id"],
            ["territories.id"],
            name="fk_ctl_territory_id_territories",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["landscape_id"],
            ["landscapes.id"],
            name="fk_ctl_landscape_id_landscapes",
        ),
        sa.UniqueConstraint(
            "territory_id",
            "landscape_id",
            "relation_type",
            name="uq_territory_landscape_relation",
        ),
        sa.CheckConstraint(
            "weight IS NULL OR (weight >= 0 AND weight <= 1)",
            name="ck_ctl_weight_range",
        ),
        sa.CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="ck_ctl_confidence_range",
        ),
    )

    op.create_index(
        "ix_ctl_territory_id",
        "connections_territories_landscapes",
        ["territory_id"],
    )
    op.create_index(
        "ix_ctl_landscape_id",
        "connections_territories_landscapes",
        ["landscape_id"],
    )
    op.create_index(
        "ix_ctl_relation_type",
        "connections_territories_landscapes",
        ["relation_type"],
    )

    # Мягкий перенос старой связи territories.landscape_id в новую M2M-таблицу.
    # Старый столбец не удаляется: он остаётся как поле обратной совместимости.
    op.execute(
        """
        INSERT INTO connections_territories_landscapes (
            territory_id,
            landscape_id,
            relation_type,
            role,
            weight,
            confidence,
            source,
            comment
        )
        SELECT
            id,
            landscape_id,
            'typical',
            'main',
            1.0000,
            1.0000,
            'migration',
            'Migrated from territories.landscape_id'
        FROM territories
        WHERE landscape_id IS NOT NULL
        ON CONFLICT (territory_id, landscape_id, relation_type) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_index("ix_ctl_relation_type", table_name="connections_territories_landscapes")
    op.drop_index("ix_ctl_landscape_id", table_name="connections_territories_landscapes")
    op.drop_index("ix_ctl_territory_id", table_name="connections_territories_landscapes")
    op.drop_table("connections_territories_landscapes")

    for table_meta in reversed(CONNECTION_TABLES):
        _drop_ontology_constraints(
            table_name=table_meta["table"],
            short_name=table_meta["short"],
            unique_name=table_meta["unique"],
        )

    for table_meta in reversed(CONNECTION_TABLES):
        _drop_ontology_columns(table_meta["table"])
