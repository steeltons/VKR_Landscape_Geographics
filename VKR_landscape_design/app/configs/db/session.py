from sqlalchemy.orm import sessionmaker

from app.configs.db.database import engine

SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine,
)