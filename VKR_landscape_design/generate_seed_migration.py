#!/usr/bin/env python3
"""
Генератор Alembic-миграции для наполнения dictionary-microservice (olms_geo)
тестовыми данными из pg_dump-дампа.

Использование:
    cd VKR_landscape_design
    python3 generate_seed_migration.py

Создаёт:
    alembic/versions/YYYYMMDDHHMM_seed_data_from_dump.py
"""

import re
import os
from datetime import datetime

DUMP_PATH = "olms_geo_localhost-2026_05_11_10_05_08-dump.sql"
OUTPUT_DIR = "alembic/versions"

SKIP_TABLES = {"public.spatial_ref_sys", "public.alembic_version"}
GEOMETRY_COLUMNS = {"geom"}


def parse_value(val, col_name):
    if val == r"\N":
        return "NULL"
    if col_name in GEOMETRY_COLUMNS:
        return f"ST_GeomFromWKB(decode('{val}', 'hex'), 4326)"
    if val in ("t", "true"):
        return "TRUE"
    if val in ("f", "false"):
        return "FALSE"
    try:
        float(val)
        return val
    except ValueError:
        pass
    escaped = val.replace("'", "''")
    return f"'{escaped}'"


def generate():
    with open(DUMP_PATH, encoding="utf-8") as f:
        content = f.read()

    # Парсим COPY-блоки
    pattern = r'^COPY (public\.\w+) \(([^)]+)\) FROM stdin;\n(.*?)\n\\.$'
    blocks = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    parsed = []
    for table, cols_str, data_str in blocks:
        if table in SKIP_TABLES:
            continue
        columns = [c.strip() for c in cols_str.split(",")]
        lines_raw = [l for l in data_str.split("\n") if l.strip()]
        rows = [line.split("\t") for line in lines_raw]
        parsed.append({"table": table, "columns": columns, "rows": rows})

    # Сортируем: основные таблицы -> таблицы связей
    main_order = [
        "public.climates", "public.foundations", "public.grounds",
        "public.landscapes", "public.plants", "public.reliefs",
        "public.soils", "public.waters", "public.file_metadata",
        "public.territories", "public.territory_geometries",
        "public.connections_landscapes_climates",
        "public.connections_landscapes_foundations",
        "public.connections_landscapes_grounds",
        "public.connections_landscapes_plants",
        "public.connections_landscapes_reliefs",
        "public.connections_landscapes_soils",
        "public.connections_landscapes_waters",
        "public.connections_territories_landscapes",
    ]
    parsed.sort(key=lambda b: main_order.index(b["table"]) if b["table"] in main_order else 99)

    rev = datetime.now().strftime("%Y%m%d%H%M")

    lines = []
    lines.append('"""seed data from pg_dump (olms_geo)')
    lines.append("")
    lines.append(f"Revision ID: {rev}")
    lines.append(f"Create Date: {datetime.now().isoformat()}")
    lines.append('"""')
    lines.append("from typing import Sequence, Union")
    lines.append("from alembic import op")
    lines.append("import sqlalchemy as sa")
    lines.append("")
    lines.append(f'revision: str = "{rev}"')
    lines.append('down_revision: Union[str, None] = None  # ⚠️ Укажите ID последней миграции dictionary!')
    lines.append("branch_labels: Union[str, Sequence[str], None] = None")
    lines.append("depends_on: Union[str, Sequence[str], None] = None")
    lines.append("")
    lines.append("")
    lines.append("def upgrade() -> None:")
    lines.append("    connection = op.get_bind()")
    lines.append("")

    for pb in parsed:
        table = pb["table"]
        cols = pb["columns"]
        rows = pb["rows"]
        lines.append(f"    # --- {table}: {len(rows)} rows ---")
        lines.append(f'    connection.execute(sa.text(f"ALTER TABLE {table} DISABLE TRIGGER ALL"))')
        lines.append("")

        BATCH = 500
        for start in range(0, len(rows), BATCH):
            batch = rows[start:start + BATCH]
            vals_list = []
            for row in batch:
                parsed_vals = [parse_value(row[i] if i < len(row) else r"\N", cols[i]) for i in range(len(cols))]
                vals_list.append("(" + ", ".join(parsed_vals) + ")")
            cols_str = ", ".join(cols)
            vals_str = ",\n            ".join(vals_list)
            lines.append(f'    connection.execute(sa.text(f"""')
            lines.append(f'        INSERT INTO {table} ({cols_str}) VALUES')
            lines.append(f'            {vals_str}')
            lines.append(f'    """))')
            lines.append("")

        lines.append(f'    connection.execute(sa.text(f"ALTER TABLE {table} ENABLE TRIGGER ALL"))')
        lines.append("")

    lines.append("")
    lines.append("def downgrade() -> None:")
    lines.append("    connection = op.get_bind()")
    lines.append("    # Удаляем данные в обратном порядке (связи -> основные)")
    for pb in reversed(parsed):
        lines.append(f'    connection.execute(sa.text(f"DELETE FROM {pb["table"]}"))')
    lines.append("    # Сброс последовательностей для таблиц с serial ID")
    for pb in parsed:
        tbl = pb["table"]
        stbl = tbl.split(".", 1)[1]
        if stbl not in ("territory_geometries", "file_metadata"):
            lines.append(f'    connection.execute(sa.text(f"ALTER SEQUENCE {stbl}_id_seq RESTART WITH 1"))')
    lines.append("")

    output = "\n".join(lines)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{rev}_seed_data_from_dump.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    total_rows = sum(len(pb["rows"]) for pb in parsed)
    print(f"✅ Migration generated: {out_path}")
    print(f"   {len(parsed)} tables, {total_rows} rows")
    for pb in parsed:
        print(f"     {pb['table']}: {len(pb['rows'])} rows")


if __name__ == "__main__":
    generate()
