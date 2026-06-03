from __future__ import annotations

import time
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        started_at = time.perf_counter()

        logger.info(
            'Request started [%s] %s %s',
            request_id,
            request.method,
            request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
            logger.exception(
                'Request failed [%s] %s %s in %sms',
                request_id,
                request.method,
                request.url.path,
                duration_ms,
                exc_info=exc,
            )
            raise

        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        response.headers['X-Request-ID'] = request_id
        logger.info(
            'Request completed [%s] %s %s status=%s duration=%sms',
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
