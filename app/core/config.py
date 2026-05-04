from functools import lru_cache

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class AppSettings(BaseModel):
    name: str = 'SmartEdu Assistant API'
    version: str = '0.1.0'
    description: str = 'API for the SmartEdu Assistant project'
    api_v1_prefix: str = '/api/v1'
    debug: bool = False


class DatabaseSettings(BaseModel):
    echo: bool = False
    host: str = '127.0.0.1'
    port: int = 5432
    name: str = 'smartedu'
    user: str | None = None
    password: str | None = None

    @computed_field
    @property
    def database_url(self) -> str:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_nested_delimiter='__',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
