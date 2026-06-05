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
- uv
- Ruff
- pre-commit

## Переменные среды

Скопируйте `.env.example` в `.env` и задайте свои значения.

Ключевые переменные для запуска через Docker Compose:

- `BACKEND_IMAGE` - образ backend, опубликованный в Docker Hub.
- `DB__NAME` - имя базы данных PostgreSQL.
- `DB__USER` - пользователь PostgreSQL.
- `DB__PASSWORD` - пароль PostgreSQL.
- `AUTH__SECRET_KEY` - секрет для подписи JWT.
- `RBAC__ADMIN_EMAIL` - почта bootstrap-администратора.
- `RBAC__ADMIN_PASSWORD` - пароль bootstrap-администратора.

Локальный запуск без Docker использует `DB__HOST=127.0.0.1`. В `compose` хост базы переопределяется на `db`, поэтому дублировать значения БД в сервисах не требуется.

## Локальный запуск

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install uv
uv sync
Copy-Item .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

После запуска будут доступны:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Docker image

Файл [Dockerfile](C:\Users\Konstantin\DjangoProject\Backend\Dockerfile) собран по мотивам презентации:

- базовый образ `python:3.13-slim`;
- multi-stage сборка;
- установка `uv` через копирование бинарника из официального `uv`-image;
- кэширование слоев через ранний `COPY pyproject.toml` и cache mount для `uv`;
- отдельный пользователь `app`;
- `curl` для `HEALTHCHECK`.

Почему выбран `python:3.13-slim`: по данным Docker Hub на 4 июня 2026 года у него меньше найденных уязвимостей и меньший размер, чем у `python:3.13-slim-bookworm`.

Ссылки:

- [python:3.13-slim tags](https://hub.docker.com/_/python/tags?name=3.13-slim)
- [python:3.13-slim-bookworm tags](https://hub.docker.com/_/python/tags?name=3.13-slim-bookworm)
- [python:3.13-slim vulnerabilities](https://hub.docker.com/layers/library/python/3.13-slim/images/sha256-7d8999b140f22939451e00b79c0fd86f13d0bc0577b369f8212fce063101fb2a)
- [python:3.13-slim-bookworm vulnerabilities](https://hub.docker.com/layers/library/python/3.13-slim-bookworm/images/sha256-478b0d85e308826ab88ec54c3492beb64116036031a413247db5b530fa3e2e14)

### Сборка и публикация

```powershell
docker login
docker build -t <dockerhub-user>/smartedu-assistant-backend:latest .
docker push <dockerhub-user>/smartedu-assistant-backend:latest
```

После публикации укажите тот же тег в `.env`:

```env
BACKEND_IMAGE=docker.io/<dockerhub-user>/smartedu-assistant-backend:latest
```

## Docker Compose

Файл [compose.yaml](C:\Users\Konstantin\DjangoProject\Backend\compose.yaml) поднимает:

- `db` на `postgres:18` с постоянным томом и healthcheck;
- `migrations` для `alembic upgrade head`;
- `rbac` для создания ролей, разрешений и bootstrap-admin;
- `api` с запуском через Gunicorn на `0.0.0.0:8000`;
- `nginx` как reverse proxy с единственным внешним портом `80`.

Особенности реализации:

- общая конфигурация backend-сервисов вынесена в `x-back-service`;
- базовый образ backend вынесен в `x-back-image`;
- уменьшение дублирования сделано через YAML anchors;
- никакие сервисы не используют `build`, все образы должны тянуться из Docker Hub;
- наружу публикуется только `80:80`.

### Запуск

```powershell
Copy-Item .env.example .env
docker compose up
```

### Что важно для фронтендеров

Frontend-команде достаточно:

1. Скопировать `.env.example` в `.env`.
2. Указать актуальный `BACKEND_IMAGE` из Docker Hub.
3. При необходимости поменять `AUTH__SECRET_KEY`, `RBAC__ADMIN_EMAIL`, `RBAC__ADMIN_PASSWORD`.
4. Запустить `docker compose up`.

После старта:

- корень `http://localhost/` отдает [index.html](C:\Users\Konstantin\DjangoProject\Backend\nginx\html\index.html);
- API доступно по префиксу `http://localhost/api`;
- Swagger UI доступно по адресу `http://localhost/api/v1/docs`.

## Миграции

```powershell
uv run alembic revision --autogenerate -m "add new entity"
uv run alembic upgrade head
uv run alembic downgrade -1
```

## Проверка качества

```powershell
uv run ruff check .
uv run ruff format .
uv run pre-commit run --all-files
```
