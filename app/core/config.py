from functools import lru_cache

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_SETTINGS_CONFIG = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
    extra='ignore',
)


class AppSettings(BaseSettings):
    name: str = Field(default='SmartEdu Assistant API', validation_alias='APP_NAME')
    version: str = Field(default='0.1.0', validation_alias='APP_VERSION')
    description: str = Field(
        default='API for the SmartEdu Assistant project',
        validation_alias='APP_DESCRIPTION',
    )
    api_v1_prefix: str = Field(default='/api/v1', validation_alias='API_V1_PREFIX')
    debug: bool = Field(default=False, validation_alias='DEBUG')

    model_config = BASE_SETTINGS_CONFIG


class DatabaseSettings(BaseSettings):
    echo: bool = Field(default=False, validation_alias='DB_ECHO')
    host: str = Field(default='127.0.0.1', validation_alias='POSTGRES_HOST')
    port: int = Field(default=5432, validation_alias='POSTGRES_PORT')
    name: str = Field(default='smartedu', validation_alias='POSTGRES_DB')
    user: str = Field(default='postgres', validation_alias='POSTGRES_USER')
    password: str = Field(default='postgres', validation_alias='POSTGRES_PASSWORD')

    model_config = BASE_SETTINGS_CONFIG

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


class Settings(BaseModel):
    app: AppSettings
    db: DatabaseSettings


@lru_cache
def get_settings() -> Settings:
    return Settings(app=AppSettings(), db=DatabaseSettings())


settings = get_settings()
