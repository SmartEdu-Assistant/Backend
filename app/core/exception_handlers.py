from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import DomainValidationError, EntityNotFoundError


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


async def domain_validation_exception_handler(
    _: Request,
    exc: DomainValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={'detail': exc.message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(EntityNotFoundError, entity_not_found_exception_handler)
    app.add_exception_handler(
        DomainValidationError,
        domain_validation_exception_handler,
    )
