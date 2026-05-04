from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.routers.api import api_router
from app.routers.health import router as health_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    debug=settings.app.debug,
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(api_router)


@app.get('/', tags=['root'])
async def root() -> dict[str, str]:
    return {'message': 'Hello. This is SmartEdu Assistant'}
