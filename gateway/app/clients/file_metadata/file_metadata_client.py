import logging
import uuid

import httpx

from app.clients.file_metadata.file_metadata_dto import FileMetadataCreateRqDto
from app.configs.config import settings


logger = logging.getLogger(__name__)


class FileMetadataClient:
    def __init__(self) -> None:
        self.users_service_url = settings.users_service_url.rstrip("/")
        self.dictionary_service_url = settings.dictionary_service_url.rstrip("/")
        self.timeout = settings.request_timeout_seconds

    async def save_to_user_microservice(self, *, file_id: uuid.UUID, request: FileMetadataCreateRqDto):
        logger.info("START FileMetadataClient::save_to_user_microservice: file_id=%s", file_id)

        await self._save(base_url=self.users_service_url, file_id=file_id, request=request)

        logger.info("END FileMetadataClient::save_to_user_microservice: file_id=%s", file_id)

    async def save_to_dictionary_microservice(self, *, file_id: uuid.UUID, request: FileMetadataCreateRqDto):
        logger.info("START FileMetadataClient::save_to_dictionary_microservice: file_id=%s", file_id)

        await self._save(base_url=self.dictionary_service_url, file_id=file_id, request=request)

        logger.info("END FileMetadataClient::save_to_dictionary_microservice: file_id=%s", file_id)

    async def _save(self, *, base_url: str, file_id: uuid.UUID, request: FileMetadataCreateRqDto):
        url = f"{base_url}/api/v1/files/{file_id}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=request.model_dump())

        response.raise_for_status()