from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import BinaryIO
from urllib.parse import urlparse, urlunparse
from uuid import uuid4

from minio import Minio
from minio.error import S3Error

from olms_minio_component.config import MinioComponentSettings, get_minio_settings
from olms_minio_component.exceptions import OlmsMinioDeleteError, OlmsMinioDownloadError, OlmsMinioFileNotFoundError, OlmsMinioUploadError
from olms_minio_component.models import FileStatInfo, StoredFileInfo


class OlmsMinioComponent:

    def __init__(self, settings: MinioComponentSettings | None = None, client: Minio | None = None) -> None:
        self.settings = settings or get_minio_settings()

        self.client = client or Minio(
            endpoint=self.settings.sdk_endpoint,
            access_key=self.settings.access_key,
            secret_key=self.settings.secret_key,
            secure=self.settings.sdk_secure,
            region=self.settings.region,
        )

        if self.settings.auto_create_bucket:
            self.ensure_bucket_exists()

    def ensure_bucket_exists(self) -> None:
        if not self.client.bucket_exists(self.settings.bucket_name):
            self.client.make_bucket(bucket_name= self.settings.bucket_name, location= self.settings.region,)

    def upload_bytes(
        self,
        *,
        content: bytes,
        original_filename: str,
        file_group: str,
        content_type: str | None = None,
        object_name: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StoredFileInfo:
        stream = BytesIO(content)

        return self.upload_stream(
            stream=stream,
            size=len(content),
            original_filename=original_filename,
            file_group=file_group,
            content_type=content_type,
            object_name=object_name,
            metadata=metadata,
        )

    def upload_stream(
        self,
        *,
        stream: BinaryIO,
        size: int,
        original_filename: str,
        file_group: str,
        content_type: str | None = None,
        object_name: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StoredFileInfo:
        if object_name is None:
            object_name = self.build_object_name(
                file_group=file_group,
                original_filename=original_filename,
            )

        try:
            result = self.client.put_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
                data=stream,
                length=size,
                content_type=content_type or "application/octet-stream",
                metadata=metadata,
            )
        except S3Error as exc:
            raise OlmsMinioUploadError(
                f"Failed to upload object '{object_name}': {exc}"
            ) from exc

        return StoredFileInfo(
            bucket_name=self.settings.bucket_name,
            object_name=object_name,
            original_filename=original_filename,
            content_type=content_type,
            file_group=file_group,
            size=size,
            etag=result.etag,
            version_id=result.version_id,
        )

    def upload_local_file(
        self,
        *,
        file_path: str | Path,
        file_group: str,
        content_type: str | None = None,
        object_name: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> StoredFileInfo:
        path = Path(file_path)

        with path.open("rb") as file:
            return self.upload_stream(
                stream=file,
                size=path.stat().st_size,
                original_filename=path.name,
                file_group=file_group,
                content_type=content_type,
                object_name=object_name,
                metadata=metadata,
            )

    def download_bytes(self, *, object_name: str) -> bytes:
        response = None

        try:
            response = self.client.get_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
            )

            return response.read()

        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject"}:
                raise OlmsMinioFileNotFoundError(
                    f"Object not found: {object_name}"
                ) from exc

            raise OlmsMinioDownloadError(
                f"Failed to download object '{object_name}': {exc}"
            ) from exc

        finally:
            if response is not None:
                response.close()
                response.release_conn()

    def delete_object(self, *, object_name: str) -> None:
        try:
            self.client.remove_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
            )
        except S3Error as exc:
            raise OlmsMinioDeleteError(
                f"Failed to delete object '{object_name}': {exc}"
            ) from exc

    def object_exists(self, *, object_name: str) -> bool:
        try:
            self.client.stat_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
            )
            return True
        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject"}:
                return False

            raise

    def stat_object(self, *, object_name: str) -> FileStatInfo:
        try:
            stat = self.client.stat_object(
                bucket_name=self.settings.bucket_name,
                object_name=object_name,
            )
        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject"}:
                raise OlmsMinioFileNotFoundError(
                    f"Object not found: {object_name}"
                ) from exc

            raise OlmsMinioDownloadError(
                f"Failed to stat object '{object_name}': {exc}"
            ) from exc

        return FileStatInfo(
            bucket_name=self.settings.bucket_name,
            object_name=object_name,
            size=stat.size,
            etag=stat.etag,
            content_type=stat.content_type,
            last_modified=stat.last_modified,
            metadata=dict(stat.metadata or {}),
        )

    def get_presigned_get_url(
        self,
        *,
        object_name: str,
        expires_seconds: int | None = None,
    ) -> str:
        expires = timedelta(
            seconds=expires_seconds
            or self.settings.presigned_url_expires_seconds
        )

        url = self.client.presigned_get_object(
            bucket_name=self.settings.bucket_name,
            object_name=object_name,
            expires=expires,
        )

        return self._rewrite_public_url(url)

    def get_presigned_put_url(
        self,
        *,
        object_name: str,
        expires_seconds: int | None = None,
    ) -> str:
        expires = timedelta(
            seconds=expires_seconds
            or self.settings.presigned_url_expires_seconds
        )

        url = self.client.presigned_put_object(
            bucket_name=self.settings.bucket_name,
            object_name=object_name,
            expires=expires,
        )

        return self._rewrite_public_url(url)

    def build_object_name(
        self,
        *,
        file_group: str,
        original_filename: str,
    ) -> str:
        safe_group = self._sanitize_path_part(file_group)
        suffix = Path(original_filename).suffix.lower()

        if len(suffix) > 16:
            suffix = ""

        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        file_id = uuid4().hex

        return f"{safe_group}/{date_path}/{file_id}{suffix}"

    def _rewrite_public_url(self, url: str) -> str:
        if not self.settings.public_endpoint:
            return url

        source = urlparse(url)
        target = urlparse(self.settings.public_endpoint)

        return urlunparse(
            (
                target.scheme or source.scheme,
                target.netloc or source.netloc,
                source.path,
                source.params,
                source.query,
                source.fragment,
            )
        )

    def _sanitize_path_part(self, value: str) -> str:
        cleaned = value.strip().replace("\\", "/")
        cleaned = cleaned.strip("/")

        if not cleaned:
            return "common"

        allowed = []

        for char in cleaned:
            if char.isalnum() or char in {"-", "_", "/"}:
                allowed.append(char)
            else:
                allowed.append("_")

        return "".join(allowed)