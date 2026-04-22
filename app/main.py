from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import create_db_and_tables
from app.routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="SmartEdu Assistant API",
    version="1.0.0",
    description="API для цифрового ассистента преподавателя",
    lifespan=lifespan
)

app.include_router(items.router)


@app.get("/")
async def root():
    """
    Корневой эндпоинт
    Возвращает приветствие
    """
    return {"message": "Hello. This is SmartEdu Assistant"}


@app.get("/health")
async def health_check():
    """
    Проверка работоспособности сервера
    """
    return {"status": "healthy", "service": "SmartEdu Assistant"}
