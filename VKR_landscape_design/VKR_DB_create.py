import psycopg2
import pandas as pd
from passlib.context import CryptContext
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Подключение к серверу PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",  # Подключаемся к базе данных по умолчанию
    user="postgres",  # Пользователь с правами на создание БД
    password="1234",  # Пароль пользователя
    host="localhost"  # Хост, например, "localhost"
)

# Устанавливаем уровень изоляции транзакции
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Создаем курсор
cursor = conn.cursor()

# Имя новой базы данных
new_db_name = "VKR"

# Создаем новую базу данных
cursor.execute(f"DROP DATABASE IF EXISTS {new_db_name}")
cursor.execute(f"CREATE DATABASE {new_db_name}")

# Закрываем соединение
cursor.close()
conn.close()

print(f"База данных '{new_db_name}' успешно создана.")