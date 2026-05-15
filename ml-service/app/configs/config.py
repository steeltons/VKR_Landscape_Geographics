from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Landscape GIS ML Service"
    app_host: str = "0.0.0.0"
    app_port: int = 8030
    app_debug: bool = True
    debug_level: str = "info"

    gateway_url: str = "http://localhost:8080"
    request_timeout_seconds: int = 120

    dictionary_microservice_base_url: str = "http://localhost:8020"
    dictionary_microservice_timeout: int = 120

    training_database_url: str = "postgresql+psycopg://geo:test@localhost:6000/olms_geo"

    model_minio_root_dir: str = "ml_service/models"
    model_current_version: str = "default"

    default_model_name: str = "landscape_recommender"
    model_filename: str = "landscape_recommender.cbm"
    model_metrics_filename: str = "training_metrics.json"
    model_dataset_filename: str = "training_dataset.csv"

    model_local_tmp_dir: str = "/tmp/olms-ml-service"

    catboost_train_dir: str = "/tmp/olms-ml-service/catboost_info"

    model_current_version_filename: str = "current.json"
    model_fail_fast_on_startup: bool = False

    @property
    def active_model_object_name(self) -> str:
        return self.build_model_object_name(self.model_current_version)

    def build_model_object_name(self, version: str) -> str:
        return self._build_minio_object_name(
            version=version,
            filename=self.model_filename,
        )

    def build_metrics_object_name(self, version: str) -> str:
        return self._build_minio_object_name(
            version=version,
            filename=self.model_metrics_filename,
        )

    def build_dataset_object_name(self, version: str) -> str:
        return self._build_minio_object_name(
            version=version,
            filename=self.model_dataset_filename,
        )

    def build_version_dir(self, version: str) -> str:
        normalized_version = self._normalize_version(version)
        return f"{self.model_minio_root_dir}/{normalized_version}"

    def build_current_model_version_object_name(self) -> str:
        return f"{self.model_minio_root_dir}/{self.model_current_version_filename}"

    def _build_minio_object_name(
        self,
        *,
        version: str,
        filename: str,
    ) -> str:
        return f"{self.build_version_dir(version)}/{filename}"

    def _normalize_version(self, version: str) -> str:
        normalized = version.strip().replace("\\", "/").strip("/")

        if not normalized:
            return "default"

        safe_chars = []

        for char in normalized:
            if char.isalnum() or char in {"-", "_", ".", "/"}:
                safe_chars.append(char)
            else:
                safe_chars.append("_")

        return "".join(safe_chars)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()