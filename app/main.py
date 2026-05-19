from fastapi import FastAPI

from app.core.config import settings
from app.db import metadata
from app.core.exception_handlers import register_exception_handlers
from app.routers.api import api_router
from app.routers.health import router as health_router


app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    debug=settings.app.debug,
)
app.state.metadata = metadata

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(api_router)


@app.get('/', tags=['root'])
async def root() -> dict[str, str]:
    return {'message': 'Hello. This is SmartEdu Assistant'}
