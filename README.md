# SmartEdu Assistant Backend

Backend-часть проекта SmartEdu Assistant на `FastAPI`.

## Стек

- Python 3.13+
- FastAPI
- SQLModel
- SQLAlchemy Async
- PostgreSQL
- asyncpg
- Alembic
- PyJWT
- pwdlib
- Ruff
- pre-commit

## Переменные среды

Скопируйте `.env.example` в `.env` и задайте значения переменных.

| Переменная | Тип | Описание | Пример |
|---|---|---|---|
| `APP__NAME` | `str` | Название приложения | `SmartEdu Assistant API` |
| `APP__VERSION` | `str` | Версия API | `0.1.0` |
| `APP__DESCRIPTION` | `str` | Описание для OpenAPI | `API for the SmartEdu Assistant project` |
| `APP__API_V1_PREFIX` | `str` | Префикс API | `/api/v1` |
| `APP__DEBUG` | `bool` | Режим отладки | `false` |
| `DB__DRIVER` | `str` | SQLAlchemy driver | `postgresql+asyncpg` |
| `DB__ECHO` | `bool` | Логирование SQL-запросов | `false` |
| `DB__HOST` | `str` | Хост PostgreSQL | `127.0.0.1` |
| `DB__PORT` | `int` | Порт PostgreSQL | `5432` |
| `DB__NAME` | `str` | Имя базы данных | `smartedu` |
| `DB__USER` | `str` | Пользователь PostgreSQL | `postgres` |
| `DB__PASSWORD` | `str` | Пароль PostgreSQL | `postgres` |
| `AUTH__SECRET_KEY` | `str` | Секрет для подписи JWT, минимум 32 символа | `generate-with-openssl` |
| `AUTH__ALGORITHM` | `str` | Алгоритм подписи JWT | `HS256` |
| `AUTH__ACCESS_TOKEN_TTL_MINUTES` | `int` | Время жизни access-токена | `15` |
| `AUTH__REFRESH_TOKEN_TTL_DAYS` | `int` | Время жизни refresh-токена | `7` |
| `AUTH__REFRESH_COOKIE_NAME` | `str` | Имя cookie с refresh-токеном | `refresh_token` |
| `AUTH__REFRESH_COOKIE_SECURE` | `bool` | Флаг `secure` для refresh-cookie | `true` |
| `AUTH__REFRESH_COOKIE_SAMESITE` | `str` | Значение `SameSite` для refresh-cookie | `lax` |
| `AUTH__REFRESH_COOKIE_DOMAIN` | `str` | Домен refresh-cookie | `example.com` |
| `AUTH__REFRESH_COOKIE_PATH` | `str` | Путь refresh-cookie | `/` |
| `AUTH__VERIFICATION_TOKEN_TTL_HOURS` | `int` | Время жизни токена подтверждения аккаунта в часах | `24` |
| `AUTH__REQUIRE_VERIFIED_ACCOUNT` | `bool` | Требовать подтверждение email перед логином | `true` |
| `CORS__ALLOW_ORIGINS` | `list[str]` | Список допустимых origin для CORS | `["http://localhost:3000","http://127.0.0.1:3000"]` |
| `CORS__ALLOW_CREDENTIALS` | `bool` | Разрешать отправку credentials в CORS-запросах | `true` |
| `CORS__ALLOW_METHODS` | `list[str]` | Разрешенные HTTP-методы для CORS | `["GET","POST","PUT","PATCH","DELETE","OPTIONS"]` |
| `CORS__ALLOW_HEADERS` | `list[str]` | Разрешенные HTTP-заголовки для CORS | `["*"]` |
| `RATE_LIMIT__ENABLED` | `bool` | Включить ограничение частоты запросов | `true` |
| `RATE_LIMIT__DEFAULT_LIMIT` | `str` | Лимит запросов по умолчанию | `100/minute` |
| `SMTP__ENABLED` | `bool` | Включить отправку писем через SMTP | `false` |
| `SMTP__HOST` | `str` | SMTP-хост | `smtp.example.com` |
| `SMTP__PORT` | `int` | SMTP-порт | `587` |
| `SMTP__USERNAME` | `str` | Логин SMTP-аккаунта | `user@example.com` |
| `SMTP__PASSWORD` | `str` | Пароль SMTP-аккаунта | `change_me` |
| `SMTP__FROM_EMAIL` | `str` | Email отправителя писем | `noreply@example.com` |
| `SMTP__FROM_NAME` | `str` | Имя отправителя писем | `SmartEdu Assistant` |
| `SMTP__STARTTLS` | `bool` | Использовать STARTTLS для SMTP | `true` |
| `SMTP__SSL_TLS` | `bool` | Использовать SSL/TLS для SMTP | `false` |
| `SMTP__VALIDATE_CERTS` | `bool` | Проверять SSL-сертификаты SMTP-сервера | `true` |
| `EMAIL__TEMPLATES_DIR` | `str` | Путь к HTML-шаблонам писем | `app/templates/emails` |
| `EMAIL__FRONTEND_BASE_URL` | `str` | Базовый URL frontend для ссылок в письмах | `http://localhost:3000` |
| `RBAC__ADMIN_ROLE_NAME` | `str` | Название admin-роли | `admin` |
| `RBAC__PUBLIC_ROLE_NAME` | `str` | Название public-роли | `public` |
| `RBAC__TEACHER_ROLE_NAME` | `str` | Название teacher-роли | `teacher` |
| `RBAC__ADMIN_EMAIL` | `str` | Email bootstrap-admin пользователя | `admin@example.com` |
| `RBAC__ADMIN_PASSWORD` | `str` | Пароль bootstrap-admin пользователя | `change-me-admin-password` |
| `RBAC__ADMIN_FIRST_NAME` | `str` | Имя bootstrap-admin пользователя | `System` |
| `RBAC__ADMIN_LAST_NAME` | `str` | Фамилия bootstrap-admin пользователя | `Administrator` |

JWT-ключ можно сгенерировать так:

```powershell
openssl rand -hex 32
```

## Запуск проекта

### 1. Создать и активировать виртуальное окружение

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Установить зависимости

```powershell
pip install uv
uv sync
```

### 3. Создать `.env`

```powershell
Copy-Item .env.example .env
```

### 4. Подготовить PostgreSQL

```sql
CREATE DATABASE smartedu;
```

### 5. Применить миграции

```powershell
uv run alembic upgrade head
```

### 6. Запустить приложение

```powershell
uv run uvicorn app.main:app --reload
```

После запуска будут доступны:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Миграции

Создать новую миграцию:

```powershell
uv run alembic revision --autogenerate -m "add new entity"
```

Применить миграции:

```powershell
uv run alembic upgrade head
```

Откатить последнюю миграцию:

```powershell
uv run alembic downgrade -1
```

## Проверка качества

```powershell
uv run ruff check .
uv run ruff format .
uv run pre-commit run --all-files
```
