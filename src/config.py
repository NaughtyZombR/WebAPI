from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="/etc/secrets/.env", env_file_encoding="utf-8")

    database_sqlite_url: str
    secret_key_jwt: str
    secret_verification_token: str
    secret_reset_token: str


@lru_cache
def get_settings() -> Settings:
    return Settings()
