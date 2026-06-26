#!/usr/bin/env bash
#
# Локальный запуск микросервиса VKR_landscape_design (без Docker)
# Предварительно должен быть запущен PostgreSQL (например, через `docker compose up db -d`)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Локальный запуск user-microservice ==="

# 1️. Активируем виртуальное окружение (создаём, если нет)
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "--> Создаю виртуальное окружение..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

source "$SCRIPT_DIR/.venv/bin/activate"
echo "--> Виртуальное окружение активировано"

# 2️. Устанавливаем кастомную библиотеку jwt-guard
if [ -d "$PROJECT_DIR/jwt-guard" ]; then
    echo "--> Устанавливаю jwt-guard..."
    pip install -e "$PROJECT_DIR/jwt-guard" --quiet
fi

# 3️. Устанавливаем зависимости
echo "--> Устанавливаю зависимости..."
pip install -r "$SCRIPT_DIR/requirements.txt" --quiet

# 4️. Переходим в папку микросервиса
cd "$SCRIPT_DIR"

# 5️. Загружаем переменные из .env (если есть)
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "--> Загружаю .env..."
    set -a
    source "$SCRIPT_DIR/.env"
    set +a
fi

# 6️. Применяем миграции alembic (если БД доступна)
echo "--> Проверяю доступность БД..."
if pg_isready -h "${DB_HOST:-localhost}" -p "${DB_PORT:-6000}" -U "${DB_USER:-geo}" > /dev/null 2>&1; then
    echo "--> Применяю миграции alembic..."
    alembic upgrade head
else
    echo "⚠️  БД недоступна (${DB_HOST:-localhost}:${DB_PORT:-6000}), миграции не применены."
    echo "   Запустите БД: docker compose up db -d (из корня проекта)"
fi

# 7️. Запускаем сервер
echo "--> Запускаю FastAPI сервер на 0.0.0.0:${APP_PORT:-8000}..."
uvicorn main:app \
    --host "${APP_HOST:-0.0.0.0}" \
    --port "${APP_PORT:-8000}" \
    --reload \
    --log-level "${APP_DEBUG:-info}"
