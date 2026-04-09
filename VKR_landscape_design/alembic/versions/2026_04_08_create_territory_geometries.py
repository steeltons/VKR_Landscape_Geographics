"""create territory_geometries table

Revision ID: 0001_create_territory_geometries
Revises: tsvetkov.stas
Create Date: 2026-04-08
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "0001_create_territory_geometries"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "territory_geometries",
        sa.Column("geometry_id", sa.BigInteger(), primary_key=True),
        sa.Column(
            "territory_id",
            sa.BigInteger(),
            sa.ForeignKey("territories.territory_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "geom",
            Geometry(geometry_type="MULTIPOLYGON", srid=4326, spatial_index=False),
            nullable=False,
        ),
        sa.Column(
            "version",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("1"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_index(
        "ix_territory_geometries_territory_id",
        "territory_geometries",
        ["territory_id"],
    )

    op.create_index(
        "ix_territory_geometries_geom",
        "territory_geometries",
        ["geom"],
        postgresql_using="gist",
    )


def downgrade() -> None:
    op.drop_index("ix_territory_geometries_geom", table_name="territory_geometries")
    op.drop_index("ix_territory_geometries_territory_id", table_name="territory_geometries")
    op.drop_table("territory_geometries")