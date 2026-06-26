# ml-microservice

Микросервис ML-рекомендаций для геоинформационной системы ландшафтной географии.

**Порт:** 8030  
**Стек:** FastAPI, CatBoost, PostgreSQL/PostGIS, MinIO

---

## Зависимости

При запуске через Docker Compose всё поднимается автоматически.
При ручном запуске потребуется работающая инфраструктура:

- **PostgreSQL 15+** с PostGIS (порт 6000:5432)
- **MinIO** — S3-совместимое хранилище (порт 9000)

---

## Быстрый старт (Docker Compose)

Из корня проекта:

```bash
docker compose up -d --build ml-microservice
```

Сервис будет доступен на `http://localhost:8030`.

---

## Ручной запуск

### 1. Запустить инфраструктуру

```bash
# Из корня проекта
docker compose up db minio minio-init -d
```

### 2. Подготовить окружение

```bash
# Перейти в директорию сервиса
cd ml-service

# Создать виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# Установить локальную библиотеку для MinIO
pip install -e ../olms-minio-component

# Установить зависимости
pip install -r requirements.txt
```

### 3. Применить миграции

```bash
alembic upgrade head
```

### 4. Запустить

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8030 --reload
```

---

## Проверка

```bash
# Healthcheck
curl http://localhost:8030/health
# → {"status":"ok"}

# Список моделей (пустой, пока не обучена)
curl http://localhost:8030/api/v1/models
# → []
```

---

## Переменные окружения

Можно задать через `.env` в корне `ml-service/` или через переменные среды.

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| `APP_HOST` | `0.0.0.0` | Хост для uvicorn |
| `APP_PORT` | `8030` | Порт для uvicorn |
| `APP_DEBUG` | `true` | Режим отладки |
| `DATABASE_URL` | `postgresql+psycopg://geo:test@localhost:6000/olms_ml` | БД для хранения результатов рекомендаций |
| `TRAINING_DATABASE_URL` | `postgresql+psycopg://geo:test@localhost:6000/olms_geo` | БД со справочниками для обучения |
| `DICTIONARY_MICROSERVICE_BASE_URL` | `http://localhost:8020` | URL микросервиса справочников |
| `MINIO_ENDPOINT` | `http://localhost:9000` | Адрес MinIO |
| `MINIO_ACCESS_KEY` | `OLMS_USER` | Логин MinIO |
| `MINIO_SECRET_KEY` | `OLMS_PASSWORD` | Пароль MinIO |
| `MINIO_BUCKET_NAME` | `olms-files` | Бакет для артефактов модели |
| `MODEL_FAIL_FAST_ON_STARTUP` | `false` | Падать ли при старте, если модель не найдена |

---

## API

### Рекомендации

**`POST /api/v1/recommendations`**

Получить рекомендацию для точки на карте.

```json
{
  "point_x": 37.62,
  "point_y": 55.75,
  "task_type": "agriculture",
  "target": "wheat"
}
```

**Ответ:**

```json
{
  "score": 0.85,
  "level": "высокая",
  "recommendation": "Территория пригодна для выращивания пшеницы.",
  "reasons": ["...", "..."],
  "limitations": ["...", "..."],
  "evidence": [
    {"entity_type": "soil", "entity_id": 1, "entity_name": "Чернозём", "reason": "..."}
  ]
}
```

### Управление моделями

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/models` | Обучить модель и сохранить в MinIO |
| GET | `/api/v1/models` | Список всех версий модели |
| GET | `/api/v1/models/actual` | Метаданные активной модели |
| GET | `/api/v1/models/{version}` | Метаданные конкретной версии |
| POST | `/api/v1/models/activation/{version}` | Активировать версию |
| GET | `/health` | Healthcheck |

---

## Структура проекта

```
app/
├── main.py                          # Точка входа FastAPI
├── configs/
│   └── config.py                    # Настройки (pydantic-settings)
├── persistence/
│   ├── dictionary_microservice_client.py  # HTTP-клиент к dictionary
│   └── models.py                    # SQLAlchemy модели
├── service/
│   ├── health/
│   │   └── health_controller.py
│   ├── recommendation/
│   │   ├── recommendation_controller.py
│   │   ├── recommendation_dto.py
│   │   ├── recommendation_dto_mapper.py
│   │   └── recommendation_service.py
│   └── model/
│       ├── model_controller.py
│       ├── model_dto.py
│       └── model_service.py
└── ml/
    ├── features/
    │   ├── feature_builder.py
    │   ├── feature_schema.py
    │   └── encoders.py
    ├── models/
    │   ├── base_model.py
    │   ├── catboost_model.py
    │   └── model_registry.py
    ├── pipelines/
    │   ├── recommendation_pipeline.py
    │   ├── explanation_builder.py
    │   ├── evidence_builder.py
    │   └── recommendation_text_builder.py
    ├── artifacts/
    │   └── model_artifact_storage.py
    └── training/
        ├── dataset_builder.py
        ├── weak_labeler.py
        └── model_trainer.py
```

---

## Работа с моделями

- Артефакты модели хранятся в **MinIO** (`olms-files/ml_service/models/`)
- Актуальная версия определяется файлом `current.json` в MinIO
- Модель загружается в память при старте сервиса
- Если модель не найдена, сервис продолжает работу (при `MODEL_FAIL_FAST_ON_STARTUP=false`)
