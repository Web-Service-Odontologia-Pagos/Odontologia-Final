import logging
import uuid
import contextvars
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request

# Context variable to store correlation id per request
correlation_id_ctx: contextvars.ContextVar | None = contextvars.ContextVar("correlation_id", default=None)


class CorrelationIdFilter(logging.Filter):
    """Logging filter that injects `correlation_id` into LogRecord objects.

    The filter reads the value from a context variable set by the middleware.
    If no id is set, a dash '-' is used.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            cid = correlation_id_ctx.get()
        except Exception:
            cid = None
        record.correlation_id = cid if cid else "-"
        return True


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware that ensures each request has a correlation id.

    - Reads `X-Correlation-ID` header if present, otherwise generates a UUID4 string.
    - Stores it in a contextvar so the `CorrelationIdFilter` can include it in logs.
    - Adds `X-Correlation-ID` header to the response.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        header = request.headers.get("x-correlation-id")
        cid = header if header else str(uuid.uuid4())
        correlation_id_ctx.set(cid)
        response = await call_next(request)
        # Ensure the correlation id is returned to the caller
        response.headers.setdefault("X-Correlation-ID", cid)
        return response


__all__ = ["CorrelationIdMiddleware", "CorrelationIdFilter", "correlation_id_ctx"]
