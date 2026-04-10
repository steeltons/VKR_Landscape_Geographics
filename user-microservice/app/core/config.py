from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / '.env',
        env_file_encoding= 'utf-8',
        case_sensitive= False,
        extra= 'ignore'
    )

    app_name: str = "Landscape Users API"
    app_host: str = "0.0.0.0"
    app_port: int = 8010
    app_debug: bool = True

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

if __name__ == "__main__":
    print(settings)
    print(settings.model_config)
    print(settings.app_name)

    print(settings.sqlalchemy_database_uri)