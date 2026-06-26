# VKR_Landscape_Geographics

Тема: Разработка системы поддержки исследований в области ландшафтной географии. Модуль вывода данных и рекомендаций

Автор: Цветков Станислав Олегович

Группа: М9124-09.04.04рпис

Научный руководитель: Артемьева Ирина Леонидовна

---
## Рабочие пользователи

- root:root <Логин,пароль> - пользователь со всеми правами

---

## Быстрый старт (одной командой)

```bash
docker compose up -d --build
```

После запуска все сервисы будут доступны:

| Сервис                         | Внутренний порт | Внешний порт |
|--------------------------------|-----------------|--------------|
| PostgreSQL + PostGIS           | 5432            | 6000         |
| MinIO (S3-совместимое хранилище) | 9000          | 9000         |
| MinIO Console (UI)             | 9001            | 9001         |
| dictionary-microservice        | 8000            | 8000         |
| user-microservice              | 8010            | 8010         |
| ml-microservice                | 8030            | 8030         |
| gateway                        | 8080            | 8080         |
| frontend (React)               | 80              | 3000         |

Gateway — единая точка входа. Все REST-запросы через порт 8080:

| Маршрут через gateway                   | Целевой сервис                  |
|-----------------------------------------|---------------------------------|
| `/dictionary-microservice/{path}`       | dictionary-microservice (8000)  |
| `/user-microservice/{path}`             | user-microservice (8010)        |
| `/ml-microservice/{path}`              | ml-microservice (8030)          |

Проверка:

```bash
curl http://localhost:8080/dictionary-microservice/api/v1/soils
```

---

## Системные требования

- **Docker** и **Docker Compose** (для запуска инфраструктуры)
- **Python 3.12** (для ручного запуска микросервисов)
- **bash / openssl** (для генерации JWT-ключей, опционально)

---

## dictionary-microservice (VKR_landscape_design)

Справочный микросервис ландшафтных данных (порт 8000).

### Ручной запуск

```bash
# 1. Запустить БД
docker compose up db -d

# 2. Перейти в микросервис
cd VKR_landscape_design

# 3. Подготовить окружение
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../jwt-guard
pip install -r requirements.txt

# 4. Применить миграции
alembic upgrade head

# 5. Запустить
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## user-microservice

Микросервис управления пользователями и авторизации (порт 8010).

### Подготовка ключей

Перед запуском сгенерировать RSA-ключи для JWT:

```bash
cd user-microservice
bash generate_keys.sh
```

### Ручной запуск

```bash
# 1. Запустить БД
docker compose up db -d

# 2. Перейти в микросервис
cd user-microservice

# 3. Подготовить окружение
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../jwt-guard
pip install -r requirements.txt

# 4. Применить миграции
alembic upgrade head

# 5. Запустить
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```

---

## ml-microservice

Микросервис ML-рекомендаций для геоинформационной системы (порт 8030).

**Зависимости:** PostgreSQL, MinIO.

### Ручной запуск

```bash
# 1. Запустить инфраструктуру (БД + S3)
docker compose up db minio minio-init -d

# 2. Перейти в микросервис
cd ml-service

# 3. Подготовить окружение
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../olms-minio-component
pip install -r requirements.txt

# 4. Применить миграции
alembic upgrade head

# 5. Запустить
uvicorn app.main:app --host 0.0.0.0 --port 8030 --reload
```

### Проверка

```bash
# healthcheck
curl http://localhost:8030/health

# список моделей (пустой, пока не обучена ни одна)
curl http://localhost:8030/api/v1/models
```

### Переменные окружения

Основные настройки (можно передать через `.env` в директории `ml-service/`):

```ini
# БД для хранения данных рекомендаций (olms_ml)
DATABASE_URL=postgresql+psycopg://geo:test@localhost:6000/olms_ml

# БД для обучения (olms_geo, справочники ландшафтов)
TRAINING_DATABASE_URL=postgresql+psycopg://geo:test@localhost:6000/olms_geo

# Микросервис справочников
DICTIONARY_MICROSERVICE_BASE_URL=http://localhost:8000

# MinIO (S3-совместимое хранилище моделей)
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=OLMS_USER
MINIO_SECRET_KEY=OLMS_PASSWORD
MINIO_BUCKET_NAME=olms-files

# Параметры модели
MODEL_FAIL_FAST_ON_STARTUP=false
```

При запуске через Docker Compose переменные подставляются из `docker-compose.yml` — `.env` не требуется.

### API модели

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/models` | Обучить модель и сохранить в MinIO |
| GET | `/api/v1/models` | Список всех версий модели |
| GET | `/api/v1/models/actual` | Метаданные актуальной модели |
| GET | `/api/v1/models/{version}` | Метаданные конкретной версии |
| POST | `/api/v1/models/activation/{version}` | Активировать версию модели |
| POST | `/api/v1/recommendations` | Получить рекомендацию |

---

## gateway

API-шлюз, проксирующий запросы к микросервисам (порт 8080).

**Маршруты:**
- `/user-microservice/{path}` → user-microservice (8010)
- `/dictionary-microservice/{path}` → dictionary-microservice (8000)
- `/ml-microservice/{path}` → ml-microservice (8030)

### Ручной запуск

```bash
# 1. Запустить инфраструктуру
docker compose up db minio minio-init -d

# 2. Перейти в gateway
cd gateway

# 3. Подготовить окружение
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../olms-minio-component
pip install -r requirements.txt

# 4. Запустить
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Проверка прокси

```bash
curl http://localhost:8080/dictionary-microservice/api/v1/soils
```

---

## frontend (VKR_landscape_react_front)

React-приложение — пользовательский интерфейс системы (порт 3000).

Через Docker Compose запускается автоматически. Внутри контейнера фронт обращается к `gateway:8080` (прокси).

### Ручной запуск

Для разработки фронт удобно запускать через `npm start` (на порту 3000 со своим dev-сервером):

```bash
# 1. Запустить бэкенд через Docker
docker compose up -d

# 2. Перейти во фронт
cd VKR_landscape_react_front

# 3. Установить зависимости
npm install --legacy-peer-deps

# 4. Запустить dev-сервер (порт 3000)
REACT_APP_API_BASE_URL=http://localhost:8080 npm start
```

Файл `public/config.js` содержит шаблон `"${REACT_APP_API_BASE_URL}"`, который подменяется при запуске в Docker (entrypoint через `envsubst`). При ручном запуске через `npm start` используется переменная окружения, либо хардкод `http://localhost:8080`.

> **Важно:** В режиме разработки убедитесь, что gateway отвечает на порту 8080.

---

## Запуск всех микросервисов вручную (без Docker)

```bash
# Терминал 1: инфраструктура
docker compose up db minio minio-init -d

# Терминал 2: dictionary
cd VKR_landscape_design
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Терминал 3: user
cd user-microservice
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload

# Терминал 4: ml
cd ml-service
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8030 --reload

# Терминал 5: gateway
cd gateway
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
