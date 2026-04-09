from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from core.config import settings


engine = create_engine(
    settings.sqlalchemy_database_uri,
    future=True,
    echo=settings.app_debug,
)

Base = declarative_base()