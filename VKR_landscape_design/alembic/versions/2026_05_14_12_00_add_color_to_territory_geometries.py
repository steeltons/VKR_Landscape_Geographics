"""add color to territory geometries

Revision ID: 2026_05_14_12_00
Revises: <PUT_PREVIOUS_REVISION_HERE>
Create Date: 2026-05-14 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2026_05_14_12_00_color"
down_revision: Union[str, None] = "20260408_1800_onto"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "territory_geometries",
        sa.Column(
            "color",
            sa.String(length=7),
            nullable=True,
            comment="Цвет отображения геометрии территории в HEX формате #FFFFFF",
        ),
    )

    # Сохраняем старое поведение: раньше цвет вычислялся по territory_id через md5.
    op.execute(
        """
        UPDATE territory_geometries
        SET color = '#' || substring(md5(territory_id::text), 1, 6)
        WHERE color IS NULL
        """
    )

    op.alter_column(
        "territory_geometries",
        "color",
        nullable=False,
    )

    op.create_check_constraint(
        "ck_territory_geometries_color_hex",
        "territory_geometries",
        "color ~ '^#[0-9A-Fa-f]{6}$'",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_territory_geometries_color_hex",
        "territory_geometries",
        type_="check",
    )

    op.drop_column("territory_geometries", "color")