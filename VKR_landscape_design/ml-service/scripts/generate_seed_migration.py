#!/usr/bin/env python3
"""
Генератор Alembic-миграции для наполнения dictionary-microservice (olms_geo)
тестовыми данными из pg_dump-дампа.

Использование:
    python ml-service/scripts/generate_seed_migration.py

Создаёт файл:
    VKR_landscape_design/alembic/versions/YYYY_MM_DD_HHMM_seed_data_from_dump.py
"""

import re
import os
from datetime import datetime

DUMP_PATH = os.path.join(os.path.dirname(__file__),
                         "../../olms_geo_localhost-2026_05_11_10_05_08-dump.sql")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__),
                          "../../VKR_landscape_design/alembic/versions")

SKIP_TABLES = {
    "public.spatial_ref_sys",
    "public.alembic_version",
}

# Таблицы, у которых нужно выключить триггеры перед вставкой (например, updated_at)
TRIGGER_TABLES = {
    "public.climates",
    "public.connections_landscapes_climates",
    "public.connections_landscapes_foundations",
    "public.connections_landscapes_grounds",
    "public.connections_landscapes_plants",
    "public.connections_landscapes_reliefs",
    "public.connections_landscapes_soils",
    "public.connections_landscapes_waters",
    "public.connections_territories_landscapes",
    "public.file_metadata",
    "public.foundations",
    "public.grounds",
    "public.landscapes",
    "public.plants",
    "public.reliefs",
    "public.soils",
    "public.territories",
    "public.territory_geometries",
    "public.waters",
}

# Колонки с геометрией — их нужно оборачивать в ST_GeomFromWKB
GEOMETRY_COLUMNS = {"geom"}


def parse_value(val: str, col_name: str) -> str:
    """Преобразует COPY-значение в SQL-литерал."""
    if val == r"\N":
        return "NULL"

    # Геометрия — WKB hex
    if col_name in GEOMETRY_COLUMNS:
        return f"ST_GeomFromWKB(decode('{val}', 'hex'), 4326)"

    # Булевы
    if val in ("t", "true"):
        return "TRUE"
    if val in ("f", "false"):
        return "FALSE"

    # Числа
    try:
        float(val)
        return val
    except ValueError:
        pass

    # Строки — экранируем одинарные кавычки
    escaped = val.replace("'", "''")
    return f"'{escaped}'"


def parse_copy_block(block: str) -> dict | None:
    """Парсит один COPY-блок из дампа. Возвращает {table, columns, rows} или None."""
    m = re.match(
        r"^COPY (public\.\w+) \((.+?)\) FROM stdin;\n(.*?)\n\\\.$",
        block,
        re.MULTILINE | re.DOTALL,
    )
    if not m:
        return None

    table = m.group(1)
    if table in SKIP_TABLES:
        return None

    columns_str = m.group(2)
    columns = [c.strip() for c in columns_str.split(",")]
    data_str = m.group(3).strip()

    rows = []
    for line in data_str.split("\n"):
        line = line.strip()
        if not line:
            continue
        # COPY использует табуляцию как разделитель
        values = line.split("\t")
        rows.append(values)

    return {"table": table, "columns": columns, "rows": rows}


def generate_migration():
    with open(DUMP_PATH, "r") as f:
        content = f.read()

    # Разделяем дамп на COPY-блоки
    blocks = re.findall(
        r"^COPY public\.\w+ \([^)]+\) FROM stdin;\n.*?\n\\\\\.$",
        content,
        re.MULTILINE | re.DOTALL,
    )

    parsed_blocks = []
    for block in blocks:
        parsed = parse_copy_block(block)
        if parsed:
            parsed_blocks.append(parsed)

    # Сортируем таблицы: сначала основные, потом связи
    main_tables = [
        "public.climates", "public.foundations", "public.grounds",
        "public.landscapes", "public.plants", "public.reliefs",
        "public.soils", "public.waters", "public.file_metadata",
        "public.territories", "public.territory_geometries",
    ]
    parsed_blocks.sort(key=lambda b: (
        0 if b["table"] in main_tables else 1,
        main_tables.index(b["table"]) if b["table"] in main_tables else 99,
    ))

    # Генерация Python-файла миграции
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M")
    revision = timestamp.replace("_", "")[:12]

    lines = []
    lines.append(f'"""seed data from pg_dump (olms_geo)')
    lines.append(f'')
    lines.append(f'Revision ID: {revision}')
    lines.append(f'Create Date: {datetime.now().isoformat()}')
    lines.append(f'"""')
    lines.append(f'')
    lines.append(f'from typing import Sequence, Union')
    lines.append(f'')
    lines.append(f'from alembic import op')
    lines.append(f'import sqlalchemy as sa')
    lines.append(f'')
    lines.append(f'')
    lines.append(f'# revision identifiers, used by Alembic.')
    lines.append(f'revision: str = "{revision}"')
    lines.append(f'down_revision: Union[str, None] = None  # Укажите ID предыдущей миграции!')
    lines.append(f'branch_labels: Union[str, Sequence[str], None] = None')
    lines.append(f'depends_on: Union[str, Sequence[str], None] = None')
    lines.append(f'')
    lines.append(f'')
    lines.append(f'def upgrade() -> None:')
    lines.append(f'    connection = op.get_bind()')
    lines.append(f'')

    for pb in parsed_blocks:
        table = pb["table"]
        short_table = table.split(".", 1)[1]
        columns = pb["columns"]
        rows = pb["rows"]

        lines.append(f"    # --- {table}: {len(rows)} rows ---")
        lines.append(f"    # Disable triggers for bulk insert")
        lines.append(f'    connection.execute(sa.text(f"ALTER TABLE {table} DISABLE TRIGGER ALL"))')
        lines.append(f"")

        # Вставляем пачками по 1000 строк
        BATCH_SIZE = 1000
        for batch_start in range(0, len(rows), BATCH_SIZE):
            batch = rows[batch_start:batch_start + BATCH_SIZE]

            values_list = []
            for row in batch:
                parsed = []
                for i, col in enumerate(columns):
                    val = row[i] if i < len(row) else r"\N"
                    parsed.append(parse_value(val, col))
                values_list.append("(" + ", ".join(parsed) + ")")

            cols_str = ", ".join(columns)
            values_str = ",\n            ".join(values_list)

            lines.append(f'    connection.execute(sa.text(f"""')
            lines.append(f'        INSERT INTO {table} ({cols_str}) VALUES')
            lines.append(f'            {values_str}')
            lines.append(f'    """))')
            lines.append(f"")

        lines.append(f"    # Re-enable triggers")
        lines.append(f'    connection.execute(sa.text(f"ALTER TABLE {table} ENABLE TRIGGER ALL"))')
        lines.append(f"")

    lines.append(f'')
    lines.append(f'def downgrade() -> None:')
    lines.append(f'    connection = op.get_bind()')
    lines.append(f'    # Удаляем все вставленные данные')
    tables_to_clear = [pb["table"] for pb in parsed_blocks]
    # В обратном порядке: сначала связи, потом основные
    for tbl in reversed(tables_to_clear):
        lines.append(f'    connection.execute(sa.text(f"DELETE FROM {tbl}"))')
    lines.append(f'    # Сбросить последовательности (если нужно)')
    for tbl in tables_to_clear:
        short = tbl.split(".", 1)[1]
        if short not in ("territory_geometries",):
            lines.append(f'    connection.execute(sa.text(f"ALTER SEQUENCE {short}_id_seq RESTART WITH 1"))')

    lines.append(f'')

    output = "\n".join(lines)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"{revision}_seed_data_from_dump.py")
    with open(out_path, "w") as f:
        f.write(output)

    print(f"✅ Migration generated: {out_path}")
    print(f"   {len(parsed_blocks)} tables processed")
    total_rows = sum(len(pb["rows"]) for pb in parsed_blocks)
    print(f"   {total_rows} total rows")

    # Статистика
    for pb in parsed_blocks:
        print(f"     {pb['table']}: {len(pb['rows'])} rows")


if __name__ == "__main__":
    generate_migration()
