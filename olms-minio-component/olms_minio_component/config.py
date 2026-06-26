from functools import lru_cache
from urllib.parse import urlparse

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioComponentSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="MINIO_",
    )

    endpoint: str = Field(default="http://localhost:9000")
    public_endpoint: str | None = Field(default=None)

    access_key: str = Field(default="olms_minio")
    secret_key: str = Field(default="olms_minio_password")

    bucket_name: str = Field(default="olms-files")
    secure: bool | None = Field(default=None)
    region: str | None = Field(default=None)

    auto_create_bucket: bool = Field(default=True)
    presigned_url_expires_seconds: int = Field(default=3600)

    @property
    def sdk_endpoint(self) -> str:
        parsed = urlparse(self.endpoint)

        if parsed.scheme:
            return parsed.netloc

        return self.endpoint

    @property
    def sdk_secure(self) -> bool:
        if self.secure is not None:
            return self.secure

        parsed = urlparse(self.endpoint)
        return parsed.scheme == "https"


@lru_cache
def get_minio_settings() -> MinioComponentSettings:
    return MinioComponentSettings()