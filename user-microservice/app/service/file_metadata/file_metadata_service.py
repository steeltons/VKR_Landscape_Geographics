import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from app.models.models import FileMetadata
from app.service.file_metadata.file_metadata_dto import FileMetadataCreateRqDto, FileMetadataRsDto
from app.service.file_metadata.file_metadata_dto_mapper import FileMetadataDtoMapper


class FileMetadataService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, file_id: uuid.UUID) -> FileMetadataRsDto:
        stmt = select(FileMetadata).where(
            FileMetadata.id == file_id,
            FileMetadata.is_active.is_(True),
        )

        entity = self.db.scalar(stmt)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File metadata not found by id: {file_id}",
            )

        return FileMetadataDtoMapper.to_rs_dto(entity)

    def create(self, file_id: uuid.UUID, dto: FileMetadataCreateRqDto) -> FileMetadataRsDto:
        entity = FileMetadataDtoMapper.to_entity(file_id, dto)

        try:
            self.db.add(entity)
            self.db.flush()
            self.db.refresh(entity)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return FileMetadataDtoMapper.to_rs_dto(entity)

    def deactivate(self, file_id: uuid.UUID):
        stmt = select(FileMetadata).where(
            FileMetadata.id == file_id,
            FileMetadata.is_active.is_(True),
        )

        entity = self.db.scalar(stmt)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File metadata not found by id: {file_id}",
            )

        try:
            entity.is_active = False
            self.db.add(entity)
            self.db.flush()
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise