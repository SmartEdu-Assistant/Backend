from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.db import AsyncSessionFactory, metadata
from app.routers.api import api_router
from app.routers.health import router as health_router
from app.services.bootstrap import RBACBootstrapper


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSessionFactory() as session:
        await RBACBootstrapper(session).bootstrap()
    yield


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    debug=settings.app.debug,
    lifespan=lifespan,
)
app.state.metadata = metadata

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(api_router)
