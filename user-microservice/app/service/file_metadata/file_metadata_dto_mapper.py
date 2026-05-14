from uuid import UUID

from app.models.models import FileMetadata
from app.service.file_metadata.file_metadata_dto import FileMetadataCreateRqDto, FileMetadataRsDto


class FileMetadataDtoMapper:

    @staticmethod
    def to_entity(file_id: UUID, dto: FileMetadataCreateRqDto) -> FileMetadata:
        return FileMetadata(
            id= file_id,
            name=dto.name,
            file_group=dto.file_group,
            mime_type=dto.mime_type,
            extension=dto.extension,
        )

    @staticmethod
    def to_rs_dto(entity: FileMetadata) -> FileMetadataRsDto:
        return FileMetadataRsDto.model_validate(entity)