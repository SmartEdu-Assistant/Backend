# SmartEdu Assistant Backend

Backend-часть проекта SmartEdu Assistant на `FastAPI`. Проект организован по слоям: роутеры работают с сервисами, сервисы инкапсулируют бизнес-логику, а репозитории отвечают за доступ к базе данных.

## Стек

- Python 3.13+
- FastAPI
- SQLModel
- SQLAlchemy Async
- PostgreSQL
- asyncpg
- Alembic
- pwdlib
- Ruff
- pre-commit

## Переменные среды

Скопируйте `.env.example` в `.env` и при необходимости измените значения.

| Переменная | Тип | Описание | Значение по умолчанию |
|---|---|---|---|
| `APP__NAME` | `str` | Название приложения | `SmartEdu Assistant API` |
| `APP__VERSION` | `str` | Версия API | `0.1.0` |
| `APP__DESCRIPTION` | `str` | Описание для OpenAPI | `API for the SmartEdu Assistant project` |
| `APP__API_V1_PREFIX` | `str` | Префикс основной версии API | `/api/v1` |
| `APP__DEBUG` | `bool` | Режим отладки FastAPI | `false` |
| `DB__ECHO` | `bool` | Логирование SQL-запросов SQLAlchemy | `false` |
| `DB__HOST` | `str` | Хост PostgreSQL | `127.0.0.1` |
| `DB__PORT` | `int` | Порт PostgreSQL | `5432` |
| `DB__NAME` | `str` | Имя базы данных | `smartedu` |
| `DB__USER` | `str` | Пользователь PostgreSQL | `postgres` |
| `DB__PASSWORD` | `str` | Пароль PostgreSQL | `postgres` |

Приложение формирует строку подключения к БД автоматически на основе этих переменных.

## Запуск проекта

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

### 4. Создать файл `.env`

```powershell
Copy-Item .env.example .env
```

### 5. Подготовить PostgreSQL

Убедитесь, что PostgreSQL запущен и база данных создана.

Пример:

```sql
CREATE DATABASE smartedu;
```

### 6. Применить миграции

```powershell
uv run alembic upgrade head
```

### 7. Запустить приложение

```powershell
uv run uvicorn app.main:app --reload
```

После запуска будут доступны:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Работа с миграциями

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

Проверка линтером и форматтером:

```powershell
uv run ruff check .
uv run ruff format .
```

Запуск pre-commit:

```powershell
uv run pre-commit run --all-files
```
