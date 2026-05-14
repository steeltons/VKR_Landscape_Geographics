import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.service.file_metadata.file_metadata_dto import FileMetadataCreateRqDto, FileMetadataRsDto
from app.service.file_metadata.file_metadata_service import FileMetadataService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/files",
    tags=["files"],
)


@router.get("/{fileId}", response_model=FileMetadataRsDto)
def get_file_metadata_by_id(fileId: UUID, db: Session = Depends(get_db)) -> FileMetadataRsDto:
    logger.debug("START FileMetadataController::get_file_metadata_by_id: fileId=%s", fileId)

    service = FileMetadataService(db)
    result = service.get_by_id(fileId)

    logger.debug("END FileMetadataController::get_file_metadata_by_id: fileId=%s, result=%s", fileId, result)

    return result


@router.post("/{fileId}", status_code=status.HTTP_201_CREATED)
def create_file_metadata(fileId: UUID, request: FileMetadataCreateRqDto, db: Session = Depends(get_db)) -> None:
    params = request.model_dump()
    logger.info("START FileMetadataController::create_file_metadata: request=%s", params)

    service = FileMetadataService(db)
    result = service.create(fileId, request)

    logger.info("END FileMetadataController::create_file_metadata: request=%s, result=%s", request, result)

@router.delete("/{fileId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file_metadata(fileId: UUID, db: Session = Depends(get_db)) -> None:
    logger.info("START FileMetadataController::delete_file_metadata: fileId=%s", fileId)

    service = FileMetadataService(db)
    service.deactivate(fileId)

    logger.info("END FileMetadataController::delete_file_metadata: fileId=%s", fileId)
