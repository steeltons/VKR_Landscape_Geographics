# Project Structure

```text
./
├── alembic.ini
├── requirements.txt
├── structure_script.py
├── project_structure.md
├── .env
└── .env.example
├── alembic/
│   ├── script.py.mako
│   ├── env.py
│   └── README
│   ├── versions/
│   │   ├── 2026_04_12_15_00_auth_table.py
│   │   └── 2026_04_10_13_00_init_script.py
├── app/
│   ├── main.py
│   ├── __init__.py
│   └── test_uploader.py
│   ├── service/
│   │   └── __init__.py
│   │   ├── auth/
│   │   │   ├── auth_dependencies.py
│   │   │   ├── password_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── refresh_session_service.py
│   │   │   ├── __init__.py
│   │   │   └── token_service.py
│   │   │   ├── controllers/
│   │   │   │   └── auth_controller.py
│   │   │   ├── dto/
│   │   │   │   └── auth_dto.py
│   │   ├── users/
│   │   │   ├── user_service.py
│   │   │   ├── user_controller.py
│   │   │   └── __init__.py
│   │   │   ├── dto/
│   │   │   │   └── user_dto.py
│   ├── models/
│   │   ├── entity_mixin.py
│   │   ├── __init__.py
│   │   └── models.py
│   ├── db/
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
├── keys/
│   ├── public_key.pem
│   └── private_key.pem
```