# SmartEdu Assistant Backend

## Описание проекта

`SmartEdu Assistant Backend` - backend-часть сервиса для цифрового ассистента преподавателя.
Проект реализован на `FastAPI` и построен по слоистой структуре:

- `core` - конфигурация и общие исключения;
- `db` - async engine, session и metadata;
- `models` - модели БД;
- `schemas` - `Base`, `Public`, `Create`, `Update` версии моделей;
- `repositories` - работа с БД;
- `services` - бизнес-логика;
- `routers` - HTTP-эндпоинты;
- `dependencies` - зависимости FastAPI.

API подключает корневой `APIRouter` с префиксом `/api/v1`, а работа со структурой БД делегирована `Alembic`.

## Состав команды

- Константин Горшков
- Виталина

## Стек

- Python 3.13+
- FastAPI
- SQLModel
- SQLAlchemy Async Engine / Async Session
- PostgreSQL
- asyncpg
- Alembic
- Ruff
- pre-commit

## Структура проекта

```text
app/
├── core/
├── db/
├── dependencies/
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
└── main.py
migrations/
.env.example
alembic.ini
pyproject.toml
run.py
```

## Переменные среды

Скопируйте `.env.example` в `.env` и при необходимости измените значения.

| Название переменной | Тип | Описание | Значение по умолчанию |
|---|---|---|---|
| `APP_NAME` | `str` | Название FastAPI-приложения | `SmartEdu Assistant API` |
| `APP_VERSION` | `str` | Версия приложения | `0.1.0` |
| `APP_DESCRIPTION` | `str` | Описание приложения для OpenAPI | `API for the SmartEdu Assistant project` |
| `API_V1_PREFIX` | `str` | Корневой префикс для доменных роутеров | `/api/v1` |
| `DEBUG` | `bool` | Режим отладки FastAPI | `false` |
| `DB_ECHO` | `bool` | Логирование SQL-запросов SQLAlchemy | `false` |
| `POSTGRES_HOST` | `str` | Хост локального PostgreSQL | `127.0.0.1` |
| `POSTGRES_PORT` | `int` | Порт PostgreSQL | `5432` |
| `POSTGRES_DB` | `str` | Имя базы данных | `smartedu` |
| `POSTGRES_USER` | `str` | Пользователь PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | `str` | Пароль PostgreSQL | `postgres` |

На основе этих значений приложение собирает строку подключения в формате:

```text
postgresql+asyncpg://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB
```

## Подготовка локальной PostgreSQL

Перед запуском приложения PostgreSQL должна быть запущена локально, а база данных уже создана.

Пример SQL-команды:

```sql
CREATE DATABASE smartedu;
```

## Установка и запуск

### 1. Создать и активировать виртуальное окружение

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Установить `uv`

```powershell
pip install uv
```

### 3. Установить зависимости

```powershell
uv sync
```

### 4. Создать `.env`

```powershell
Copy-Item .env.example .env
```

### 5. Применить миграции

```powershell
uv run alembic upgrade head
```

### 6. Запустить приложение

```powershell
uv run uvicorn app.main:app --reload
```

## Миграции Alembic

После настройки проекта структура БД не создаётся через `SQLModel.metadata.create_all()` на старте приложения.
Все изменения схемы должны выполняться через `Alembic`.

### Создать новую миграцию

```powershell
uv run alembic revision --autogenerate -m "add new entity"
```

### Применить миграции

```powershell
uv run alembic upgrade head
```

### Откатить последнюю миграцию

```powershell
uv run alembic downgrade -1
```

## Проверка проекта

### Запустить Ruff

```powershell
uv run ruff check .
uv run ruff format .
```

### Запустить pre-commit

```powershell
uv run pre-commit run --all-files
```
