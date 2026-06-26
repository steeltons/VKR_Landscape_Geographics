import logging
import mimetypes
import uuid
from pathlib import Path

from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

from olms_minio_component import OlmsMinioComponent

from app.clients.file_metadata.file_metadata_client import FileMetadataClient
from app.clients.file_metadata.file_metadata_dto import FileMetadataCreateRqDto
from app.service.file_metadata_dto import FileUploadRsDto, FileDownloadData

logger = logging.getLogger(__name__)


class FileMetadataService:
    USER_MICROSERVICE_MINIO_DIR = "user_microservice"
    DICTIONARY_MICROSERVICE_MINIO_DIR = "dictionary_microservice"

    def __init__(self) -> None:
        self.minio_component = OlmsMinioComponent()
        self.file_metadata_client = FileMetadataClient()

    async def save_user_microservice_file(
        self,
        *,
        file: UploadFile,
        file_group: str,
    ) -> FileUploadRsDto:
        file_id = uuid.uuid4()

        original_filename = self._extract_filename(file)
        mime_type = self._extract_mime_type(file)
        extension = self._extract_extension(
            filename=original_filename,
            mime_type=mime_type,
        )

        object_name = self._build_object_name(
            minio_directory=self.USER_MICROSERVICE_MINIO_DIR,
            file_id=file_id,
            extension=extension,
        )

        logger.info(
            "START FileMetadataService::save_user_microservice_file "
            "file_id=%s file_group=%s object_name=%s",
            file_id,
            file_group,
            object_name,
        )

        content = await file.read()

        await run_in_threadpool(
            self.minio_component.upload_bytes,
            content=content,
            original_filename=original_filename,
            file_group=file_group,
            content_type=mime_type,
            object_name=object_name,
            metadata={
                "file-id": str(file_id),
                "file-group": file_group,
                "minio-directory": self.USER_MICROSERVICE_MINIO_DIR,
                "original-filename": original_filename,
            },
        )

        metadata_request = FileMetadataCreateRqDto(
            name=original_filename,
            file_group=file_group,
            mime_type=mime_type,
            extension=extension,
        )

        try:
            await self.file_metadata_client.save_to_user_microservice(
                file_id=file_id,
                request=metadata_request,
            )
        except Exception:
            logger.exception(
                "Failed to save user file metadata. Rolling back MinIO object. "
                "file_id=%s object_name=%s",
                file_id,
                object_name,
            )

            await self._safe_delete_minio_object(object_name)

            raise

        result = FileUploadRsDto(file_id=str(file_id))

        logger.info(
            "END FileMetadataService::save_user_microservice_file "
            "file_id=%s file_group=%s result=%s",
            file_id,
            file_group,
            result,
        )

        return result

    async def save_dictionary_microservice_file(
        self,
        *,
        file: UploadFile,
        file_group: str,
    ) -> FileUploadRsDto:
        file_id = uuid.uuid4()

        original_filename = self._extract_filename(file)
        mime_type = self._extract_mime_type(file)
        extension = self._extract_extension(
            filename=original_filename,
            mime_type=mime_type,
        )

        object_name = self._build_object_name(
            minio_directory=self.DICTIONARY_MICROSERVICE_MINIO_DIR,
            file_id=file_id,
            extension=extension,
        )

        logger.info(
            "START FileMetadataService::save_dictionary_microservice_file "
            "file_id=%s file_group=%s object_name=%s",
            file_id,
            file_group,
            object_name,
        )

        content = await file.read()

        await run_in_threadpool(
            self.minio_component.upload_bytes,
            content=content,
            original_filename=original_filename,
            file_group=file_group,
            content_type=mime_type,
            object_name=object_name,
            metadata={
                "file-id": str(file_id),
                "file-group": file_group,
                "minio-directory": self.DICTIONARY_MICROSERVICE_MINIO_DIR,
                "original-filename": original_filename,
            },
        )

        metadata_request = FileMetadataCreateRqDto(
            name=original_filename,
            file_group=file_group,
            mime_type=mime_type,
            extension=extension,
        )

        try:
            await self.file_metadata_client.save_to_dictionary_microservice(
                file_id=file_id,
                request=metadata_request,
            )
        except Exception:
            logger.exception(
                "Failed to save dictionary file metadata. Rolling back MinIO object. "
                "file_id=%s object_name=%s",
                file_id,
                object_name,
            )

            await self._safe_delete_minio_object(object_name)

            raise

        result = FileUploadRsDto(file_id=str(file_id))

        logger.info(
            "END FileMetadataService::save_dictionary_microservice_file "
            "file_id=%s file_group=%s result=%s",
            file_id,
            file_group,
            result,
        )

        return result

    async def download_user_microservice_file(
            self,
            *,
            file_id: uuid.UUID,
    ) -> FileDownloadData | None:
        logger.debug(
            "START FileMetadataService::download_user_microservice_file file_id=%s",
            file_id,
        )

        result = await self._download_file_from_minio(
            file_id=file_id,
            minio_directory=self.USER_MICROSERVICE_MINIO_DIR,
        )

        logger.debug(
            "END FileMetadataService::download_user_microservice_file file_id=%s result=%s",
            file_id,
            result.filename if result else None,
        )

        return result

    async def download_dictionary_microservice_file(
            self,
            *,
            file_id: uuid.UUID,
    ) -> FileDownloadData | None:
        logger.debug(
            "START FileMetadataService::download_dictionary_microservice_file file_id=%s",
            file_id,
        )

        result = await self._download_file_from_minio(
            file_id=file_id,
            minio_directory=self.DICTIONARY_MICROSERVICE_MINIO_DIR,
        )

        logger.debug(
            "END FileMetadataService::download_dictionary_microservice_file file_id=%s result=%s",
            file_id,
            result.filename if result else None,
        )

        return result

    async def _download_file_from_minio(
            self,
            *,
            file_id: uuid.UUID,
            minio_directory: str,
    ) -> FileDownloadData | None:
        object_name = await self._find_minio_object_by_file_id(
            file_id=file_id,
            minio_directory=minio_directory,
        )

        if object_name is None:
            return None

        content = await run_in_threadpool(
            self.minio_component.download_bytes,
            object_name=object_name,
        )

        filename = Path(object_name).name
        media_type = self._guess_media_type(filename)

        return FileDownloadData(
            content=content,
            filename=filename,
            media_type=media_type,
        )

    async def _find_minio_object_by_file_id(
            self,
            *,
            file_id: uuid.UUID,
            minio_directory: str,
    ) -> str | None:
        prefix = f"{minio_directory}/{file_id}"

        objects = await run_in_threadpool(
            lambda: list(
                self.minio_component.client.list_objects(
                    bucket_name=self.minio_component.settings.bucket_name,
                    prefix=prefix,
                    recursive=True,
                )
            )
        )

        if not objects:
            return None

        objects = sorted(objects, key=lambda item: item.object_name)

        return objects[0].object_name

    def _guess_media_type(
            self,
            filename: str,
    ) -> str:
        media_type, _ = mimetypes.guess_type(filename)

        return media_type or "application/octet-stream"

    async def _safe_delete_minio_object(
        self,
        object_name: str,
    ) -> None:
        try:
            await run_in_threadpool(
                self.minio_component.delete_object,
                object_name=object_name,
            )
        except Exception:
            logger.exception(
                "Failed to rollback MinIO object: %s",
                object_name,
            )

    def _extract_filename(
        self,
        file: UploadFile,
    ) -> str:
        if not file.filename:
            return "file"

        return Path(file.filename).name

    def _extract_mime_type(
        self,
        file: UploadFile,
    ) -> str:
        return file.content_type or "application/octet-stream"

    def _extract_extension(
        self,
        *,
        filename: str,
        mime_type: str,
    ) -> str:
        suffix = Path(filename).suffix.lower()

        if suffix:
            return suffix

        guessed = mimetypes.guess_extension(mime_type)

        if guessed:
            return guessed.lower()

        return ".bin"

    def _build_object_name(
        self,
        *,
        minio_directory: str,
        file_id: uuid.UUID,
        extension: str,
    ) -> str:
        normalized_extension = (
            extension
            if extension.startswith(".")
            else f".{extension}"
        )

        return f"{minio_directory}/{file_id}{normalized_extension}"