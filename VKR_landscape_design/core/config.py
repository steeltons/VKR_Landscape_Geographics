from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file= '.env',
        env_file_encoding= 'utf-8',
        case_sensitive= False,
    )

    app_name: str = "Landscape GIS API"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True

    db_host: str = "localhost"
    db_port: int = 6000
    db_name: str = "olms_geo"
    db_user: str = "geo"
    db_password: str = "test"

    cors_origins: str = Field(default="http://localhost:3000")

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()