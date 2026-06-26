#!/usr/bin/env bash
#
# Скрипт для сборки и запуска микросервиса через Docker Compose
# Запускать из корня проекта (VKR_Landscape_Geographics)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Сборка и запуск user-microservice через Docker Compose ==="
echo "Контекст: $PROJECT_DIR"

cd "$PROJECT_DIR"

# Проверяем, что docker-compose.yml существует
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml не найден в корне проекта!"
    exit 1
fi

# Собираем и запускаем только нужные сервисы
echo "--> Сборка и запуск (db + user-microservice)..."
docker compose up --build -d db user-microservice

echo ""
echo "✅ Микросервис запущен!"
echo "   API:      http://localhost:8000"
echo "   Docs:     http://localhost:8000/docs"
echo "   БД:       localhost:6000"
echo ""
echo "Для остановки: docker compose down"
echo "Для просмотра логов: docker compose logs -f user-microservice"
