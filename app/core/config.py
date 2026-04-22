from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'SmartEdu Assistant API'
    app_version: str = '0.1.0'
    app_description: str = 'API for the SmartEdu Assistant project'
    api_v1_prefix: str = '/api/v1'
    debug: bool = False
    db_echo: bool = False

    postgres_host: str = '127.0.0.1'
    postgres_port: int = 5432
    postgres_db: str = 'smartedu'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            'postgresql+asyncpg://'
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
