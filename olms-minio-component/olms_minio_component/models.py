from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StoredFileInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket_name: str
    object_name: str

    original_filename: str | None = None
    content_type: str | None = None
    file_group: str | None = None

    size: int | None = None
    etag: str | None = None
    version_id: str | None = None


class FileStatInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket_name: str
    object_name: str

    size: int | None = None
    etag: str | None = None
    content_type: str | None = None
    last_modified: datetime | None = None
    metadata: dict[str, str] = {}