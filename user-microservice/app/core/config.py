from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

CORE_DIR = Path(__file__).resolve().parent
APP_DIR = CORE_DIR.parent
PROJECT_ROOT = APP_DIR.parent

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT / '.env',
        env_file_encoding= 'utf-8',
        case_sensitive= False,
        extra= 'ignore'
    )

    app_name: str = "Landscape Users API"
    app_host: str = "0.0.0.0"
    app_port: int = 8010
    app_debug: bool = True

    jwt_private_key_path: str
    jwt_algorithm: str = "RS256"
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 30

    jwt_public_key_path: str
    jwt_issuer: str | None = None
    jwt_audience: str | None = None

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

    @property
    def jwt_private_key(self) -> str:
        path = Path(self.jwt_private_key_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path.read_text(encoding="utf-8")

    @property
    def jwt_public_key(self) -> str:
        path = Path(self.jwt_public_key_path)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path.read_text(encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

if __name__ == "__main__":
    print(settings)
    print(settings.model_config)
    print(settings.app_name)

    print(settings.sqlalchemy_database_uri)