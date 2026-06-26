"""seed test data

Revision ID: 20260511_1006_seed_test_data
Revises: 20260412_1200_auth_table
Create Date: 2026-05-11 10:06:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "20260511_1006_seed_test_data"
down_revision = "20260412_1200_auth_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        text("""
            INSERT INTO public.users (id, login, email, created_at, updated_at, is_active)
            VALUES ('d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619', 'root', 'test@mail.com', '2026-05-10 14:28:23.556+00', '2026-05-10 14:28:29.084+00', true)
            ON CONFLICT (id) DO NOTHING
        """)
    )

    conn.execute(
        text("""
            INSERT INTO public.user_passwords (id, password, user_id, created_at, updated_at, is_active)
            VALUES ('d24ef5fe-6b5a-4ad6-b919-f3b4f09e2619', '$2a$12$bOFOjayZIhoMYxyBFLtPjOEhDeOs7sjzDI.Ny/duvBbITQS8b1hSS', 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619', '2026-05-10 14:29:06.515+00', '2026-05-10 14:29:08.276+00', true)
            ON CONFLICT (id) DO NOTHING
        """)
    )

    conn.execute(
        text("""
            INSERT INTO public.user_profiles (id, first_name, middle_name, last_name, age, gender, user_id, picture_id, created_at, updated_at, is_active)
            VALUES (1, 'Иван', 'Сидорович', 'Петров', 25, 'М', 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619', NULL, '2026-05-10 14:40:26.176+00', '2026-05-10 14:40:27.712+00', true)
            ON CONFLICT (id) DO NOTHING
        """)
    )

    # Все роли пользователю root
    all_authorities = [
        'ADD_USERS',
        'REMOVE_USERS',
        'EDIT_USERS',
        'GRANT_PERMISSIONS',
        'REVOKE_PERMISSIONS',
        'EDIT_DICTIONARY',
        'DELETE_DICTIONARY',
        'ML_ACCESS',
    ]

    for idx, authority in enumerate(all_authorities, start=1):
        conn.execute(
            text("""
                INSERT INTO public.user_authorities (id, authority, user_id, created_at, updated_at, is_active)
                VALUES (:id, :authority, 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619', '2026-05-10 18:53:26.208+00', '2026-05-10 18:53:28.564+00', true)
                ON CONFLICT (id) DO NOTHING
            """),
            {"id": idx, "authority": authority}
        )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text("""
            DELETE FROM public.user_authorities WHERE user_id = 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619'
        """)
    )
    conn.execute(
        text("""
            DELETE FROM public.user_profiles WHERE user_id = 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619'
        """)
    )
    conn.execute(
        text("""
            DELETE FROM public.user_passwords WHERE user_id = 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619'
        """)
    )
    conn.execute(
        text("""
            DELETE FROM public.users WHERE id = 'd24ef5fe-6b5a-4ad6-b919-f3b4f09e2619'
        """)
    )
