# VKR_Landscape_Geographics

Тема: Разработка системы поддержки исследований в области ландшафтной географии. Модуль вывода данных и рекомендаций

Автор: Цветков Станислав Олегович

Группа: М9124-09.04.04рпис

Научный руководитель: Артемьева Ирина Леонидовна

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
