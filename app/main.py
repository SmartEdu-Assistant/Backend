from fastapi import FastAPI

from app.routers import items

from app.models import create_db_and_tables


app = FastAPI(title="SmartEdu Assistant", description="Education assistant API", version="0.1.0")

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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
