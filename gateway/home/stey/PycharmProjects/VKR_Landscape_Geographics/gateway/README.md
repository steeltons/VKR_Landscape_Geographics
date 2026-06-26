# gateway

API-шлюз, проксирующий запросы к микросервисам и управляющий файлами через MinIO.

**Порт:** 8080

## Проксируемые маршруты

| Префикс | Целевой сервис | Порт |
|---|---|---|
| `/user-microservice/{path}` | user-microservice | 8010 |
| `/dictionary-microservice/{path}` | dictionary-microservice | 8000 |
| `/ml-microservice/{path}` | ml-microservice | 8011 |

## Ручной запуск

```bash
# 1. Запустить инфраструктуру (БД + MinIO)
docker compose up db minio minio-init -d

# 2. Установить локальную зависимость olms-minio-component
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../olms-minio-component

# 3. Установить остальные зависимости
pip install -r requirements.txt

# 4. Запустить
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_NAME` | `Landscape GIS Gateway` | |
| `APP_HOST` | `0.0.0.0` | |
| `APP_PORT` | `8080` | |
| `APP_DEBUG` | `true` | |
| `USERS_SERVICE_URL` | — | URL user-microservice (например `http://localhost:8010`) |
| `DICTIONARY_SERVICE_URL` | — | URL dictionary-microservice (например `http://localhost:8000`) |
| `ML_SERVICE_URL` | — | URL ml-microservice (например `http://localhost:8011`) |
| `REQUEST_TIMEOUT_SECONDS` | `120` | Таймаут запросов к микросервисам |
| `CORS_ORIGINS` | `http://localhost:3000` | Разрешённые CORS-источники |

## Проверка прокси

```bash
# Через gateway
curl http://localhost:8080/dictionary-microservice/api/v1/soils
curl http://localhost:8080/user-microservice/api/v1/auth/login
```
