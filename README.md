# SmartEdu Assistant Backend

## Описание проекта

`SmartEdu Assistant Backend` - backend-часть сервиса для цифрового ассистента преподавателя. Проект реализован на `FastAPI` и `SQLModel` и служит основой для API, бизнес-логики и хранения данных учебной платформы.

На текущем этапе в репозитории заложены:
- базовая структура FastAPI-приложения;
- модели доменной области для пользователей, курсов, групп, заданий, сдач, комментариев и оценок;
- настройка SQLite-базы данных;
- заготовки роутеров и OpenAPI-описание.

## Стек

- Python 3.13+
- FastAPI
- SQLModel
- Uvicorn
- Ruff
- pre-commit

## Состав команды

- Константин Горшков
- Виталина

## Структура проекта

- `app/main.py` - точка входа FastAPI-приложения
- `app/db/session.py` - настройка подключения к базе данных и сессий
- `app/models/models.py` - SQLModel-модели
- `app/routers/` - HTTP-роуты
- `openapi.yaml` - описание API
- `run.py` - локальный запуск приложения

## Запуск проекта

### 1. Создать и активировать виртуальное окружение

python -m venv venv
.\venv\Scripts\Activate.ps1


### 2. Установить зависимости

pip install -e .


Если editable-установка не используется, можно установить зависимости напрямую:


pip install fastapi "uvicorn[standard]" sqlmodel


### 3. Запустить приложение

Вариант через вспомогательный скрипт:


python run.py


Или напрямую через `uvicorn`:


uvicorn app.main:app --reload


### 4. Проверить, что сервис поднялся

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Проверки качества

Запуск pre-commit:


pre-commit run --all-files


Проверка Ruff:


ruff check .
ruff format .

