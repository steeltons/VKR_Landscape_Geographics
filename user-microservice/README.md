# user-microservice

Микросервис управления пользователями и авторизации.

## Ручной запуск

### Подготовка ключей

```bash
bash generate_keys.sh
```

### Запуск

```bash
docker compose up db -d
python3 -m venv .venv
source .venv/bin/activate
pip install -e ../jwt-guard
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```
