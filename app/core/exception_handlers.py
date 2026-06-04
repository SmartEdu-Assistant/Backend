from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.core.exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    DomainValidationError,
    EntityConflictError,
    EntityNotFoundError,
)
from app.core.logging import logger
from app.schemas.errors import ErrorResponse, ValidationErrorItem, ValidationErrorResponse


def _error_response(exc: AppError) -> ErrorResponse:
    return ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
    )


async def app_error_exception_handler(
    _: Request,
    exc: AppError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_response(exc).model_dump(exclude_none=True),
    )


async def entity_not_found_exception_handler(
    request: Request,
    exc: EntityNotFoundError,
) -> JSONResponse:
    return await app_error_exception_handler(request, exc)


async def domain_validation_exception_handler(
    request: Request,
    exc: DomainValidationError,
) -> JSONResponse:
    return await app_error_exception_handler(request, exc)


async def entity_conflict_exception_handler(
    request: Request,
    exc: EntityConflictError,
) -> JSONResponse:
    return await app_error_exception_handler(request, exc)


async def auth_exception_handler(
    request: Request,
    exc: AuthenticationError | AuthorizationError,
) -> JSONResponse:
    return await app_error_exception_handler(request, exc)


async def request_validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details = [
        ValidationErrorItem(
            field='.'.join(str(part) for part in error['loc']),
            message=error['msg'],
        )
        for error in exc.errors()
    ]
    response = ValidationErrorResponse(
        error_code='validation_error',
        message='Request validation failed',
        details=details,
    )
    return JSONResponse(status_code=422, content=response.model_dump())


async def http_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    response = ErrorResponse(
        error_code='http_error',
        message=str(exc.detail),
    )
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())


async def rate_limit_exception_handler(
    _: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    response = ErrorResponse(
        error_code='rate_limit_exceeded',
        message=str(exc.detail),
    )
    return JSONResponse(status_code=429, content=response.model_dump())


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        'Unhandled exception while processing %s %s',
        request.method,
        request.url.path,
        exc_info=exc,
    )
    response = ErrorResponse(
        error_code='internal_error',
        message='Internal server error',
    )
    return JSONResponse(status_code=500, content=response.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_exception_handler)
    app.add_exception_handler(EntityNotFoundError, entity_not_found_exception_handler)
    app.add_exception_handler(
        DomainValidationError,
        domain_validation_exception_handler,
    )
    app.add_exception_handler(
        EntityConflictError,
        entity_conflict_exception_handler,
    )
    app.add_exception_handler(AuthenticationError, auth_exception_handler)
    app.add_exception_handler(AuthorizationError, auth_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
