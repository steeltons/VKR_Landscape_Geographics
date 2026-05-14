import uuid

from pydantic import BaseModel, ConfigDict, Field


class FileMetadataCreateRqDto(BaseModel):

    name: str = Field(min_length=1)
    file_group: str = Field(min_length=1)
    mime_type: str = Field(min_length=1)
    extension: str = Field(min_length=1)


class FileMetadataRsDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    file_group: str
    mime_type: str
    extension: str
