from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import DomainValidationError, EntityNotFoundError
from app.db.base import metadata  # noqa: F401
from app.routers.api import api_router
from app.routers.health import router as health_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    debug=settings.debug,
    lifespan=lifespan,
)


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_exception_handler(
    _: Request,
    exc: EntityNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            'detail': f'{exc.entity_name} with id={exc.entity_id} was not found',
        },
    )


@app.exception_handler(DomainValidationError)
async def domain_validation_exception_handler(
    _: Request,
    exc: DomainValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={'detail': exc.message},
    )


app.include_router(health_router)
app.include_router(api_router)


@app.get('/', tags=['root'])
async def root() -> dict[str, str]:
    return {'message': 'Hello. This is SmartEdu Assistant'}
