from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class AppSettings(BaseModel):
    name: str = 'SmartEdu Assistant API'
    version: str = '0.1.0'
    description: str = 'API for the SmartEdu Assistant project'
    api_v1_prefix: str = '/api/v1'
    debug: bool = False


class LoggingSettings(BaseModel):
    level: str = 'INFO'
    format: str = '%(asctime)s %(levelname)s [%(name)s] %(message)s'


class DatabaseSettings(BaseModel):
    driver: str = 'postgresql+asyncpg'
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
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        ).render_as_string(hide_password=False)


class AuthSettings(BaseModel):
    secret_key: str = Field(min_length=32)
    algorithm: Literal['HS256'] = 'HS256'
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 7
    refresh_cookie_name: str = 'refresh_token'
    refresh_cookie_secure: bool = True
    refresh_cookie_samesite: Literal['lax', 'strict', 'none'] = 'lax'
    refresh_cookie_domain: str | None = None
    refresh_cookie_path: str = '/'
    verification_token_ttl_hours: int = 24
    require_verified_account: bool = True


class CorsSettings(BaseModel):
    allow_origins: list[str] = ['http://localhost:3000', 'http://127.0.0.1:3000']
    allow_credentials: bool = True
    allow_methods: list[str] = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
    allow_headers: list[str] = ['*']


class RateLimitSettings(BaseModel):
    enabled: bool = True
    default_limit: str = '100/minute'


class SmtpSettings(BaseModel):
    enabled: bool = False
    host: str = 'smtp.example.com'
    port: int = 587
    username: str = 'user@example.com'
    password: str = 'change_me'
    from_email: str = 'noreply@example.com'
    from_name: str = 'SmartEdu Assistant'
    starttls: bool = True
    ssl_tls: bool = False
    validate_certs: bool = True


class EmailSettings(BaseModel):
    templates_dir: str = 'app/templates/emails'
    frontend_base_url: str = 'http://localhost:3000'


class RbacSettings(BaseModel):
    admin_role_name: str = 'admin'
    public_role_name: str = 'public'
    teacher_role_name: str = 'teacher'
    admin_email: str = 'admin@example.com'
    admin_password: str = Field(min_length=8)
    admin_first_name: str = 'System'
    admin_last_name: str = 'Administrator'


class Settings(BaseSettings):
    app: AppSettings
    logging: LoggingSettings = LoggingSettings()
    db: DatabaseSettings
    auth: AuthSettings
    cors: CorsSettings = CorsSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()
    smtp: SmtpSettings = SmtpSettings()
    email: EmailSettings = EmailSettings()
    rbac: RbacSettings

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
