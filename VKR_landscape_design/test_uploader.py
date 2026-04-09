from db.database import Base, engine
from db.session import SessionLocal

from models.models import FileMetadata, Soil, Landscape, Ground, Plant, Relief

# FIXME Удалить перед слиянием в main/develop

def create_tables() -> None:
    Base.metadata.drop_all(bind= engine)
    Base.metadata.create_all(bind= engine)

if __name__ == "__main__":
    create_tables()

    session = SessionLocal()
    try:
        picture = FileMetadata(
            name= 'test.jpg',
            file_group= 'IMAGE',
            mime_type= 'image/jpeg',
            extension= 'jpg',
        )

        session.add(picture)
        session.flush()

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    i = 43