-- init-db.sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Тестовые учётные записи
CREATE USER olms_people_keeper WITH PASSWORD '5uthU]evx2RYV-2B].hMsH=aU>ia-2!9';
CREATE USER olms_knowledge_keeper WITH PASSWORD 'LjC_W_:V2}s.d6+uY+xae}r~#tovUmZ0';
CREATE USER olms_ml_keeper WITH PASSWORD 'bvUO-XEWnwgdH.)yt:qy#zS[{ljo8G3s';

-- Создание БД
CREATE DATABASE olms_people OWNER olms_people_keeper;
CREATE DATABASE olms_knowledge OWNER olms_knowledge_keeper;
CREATE DATABASE olms_ml OWNER olms_ml_keeper;

-- Выдача прав
GRANT ALL PRIVILEGES ON DATABASE olms_people TO olms_people_keeper;
GRANT ALL PRIVILEGES ON DATABASE olms_knowledge TO olms_knowledge_keeper;
GRANT ALL PRIVILEGES ON DATABASE olms_ml TO olms_ml_keeper;

-- Подключение к olms_people и установка pgcrypto
\c olms_people
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Подключение к olms_knowledge и установка pgcrypto
\c olms_knowledge
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Подключение к olms_geo и установка прав для ml-сервиса
\c olms_geo
CREATE EXTENSION IF NOT EXISTS pgcrypto;

GRANT USAGE ON SCHEMA public TO olms_ml_keeper;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO olms_ml_keeper;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO olms_ml_keeper;
