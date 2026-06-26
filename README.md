# VKR_Landscape_Geographics

Тема: Разработка системы поддержки исследований в области ландшафтной географии. Модуль вывода данных и рекомендаций

Автор: Цветков Станислав Олегович

Группа: М9124-09.04.04рпис

Научный руководитель: Артемьева Ирина Леонидовна

## Запуск dictionary-microservice

### Подготовка окружения

1. Создать виртуальное окружение Python:

```bash
python3 -m venv .venv
```

2. Активировать виртуальное окружение:

```bash
source .venv/bin/activate
```

3. Установить кастомную библиотеку jwt-guard из соседней директории:

```bash
pip install -e ../jwt-guard
```

4. Установить зависимости из requirements.txt:

```bash
pip install -r requirements.txt
```

### Запуск базы данных

База данных запускается через Docker Compose из корня проекта:

```bash
docker compose up db -d
```

### Применение миграций

После запуска базы данных выполнить миграции:

```bash
alembic upgrade head
```

### Запуск микросервиса

Запустить сервер через uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Микросервис будет доступен по адресу http://localhost:8000, документация API — http://localhost:8000/docs.
