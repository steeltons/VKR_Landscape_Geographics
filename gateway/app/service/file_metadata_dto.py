from dataclasses import dataclass

from pydantic import BaseModel


class FileUploadRsDto(BaseModel):
    file_id: str


@dataclass(frozen=True, slots=True)
class FileDownloadData:
    content: bytes
    filename: str
    media_type: str