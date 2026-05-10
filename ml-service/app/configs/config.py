from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "Landscape GIS ML Service"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True
    debug_level: str = "info"

    gateway_url: str = "http://localhost:8080"
    request_timeout_seconds: int = 120

    dictionary_microservice_base_url: str = "http://localhost:8020"
    dictionary_microservice_timeout: int = 120

    """
    Настройки модели ПО
    """
    default_model_name: str = "landscape_recommender"
    model_artifacts_dir: str = "app/ml/artifacts"
    training_database_url: str = "postgresql+psycopg://geo:test@localhost:6000/olms_geo"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()