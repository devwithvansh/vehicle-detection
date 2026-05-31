from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Army Vehicle Detection System"
    environment: str = "development"
    secret_key: str
    access_token_expire_minutes: int = 480
    database_url: str
    storage_dir: str = "../storage"
    cors_origins: str = "http://localhost:5173"
    default_admin_username: str = "admin"
    default_admin_password: str = "Admin@12345"
    yolo_model_path: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
