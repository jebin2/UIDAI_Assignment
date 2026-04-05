import logging
import uuid
from time import monotonic

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context import request_id

logger = logging.getLogger(__name__)


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = str(uuid.uuid4())
        token = request_id.set(rid)
        start = monotonic()

        logger.info("REQUEST  method=%s path=%s", request.method, request.url.path)

        response = await call_next(request)

        elapsed_ms = round((monotonic() - start) * 1000, 1)
        logger.info("RESPONSE status=%s path=%s duration_ms=%s", response.status_code, request.url.path, elapsed_ms)

        request_id.reset(token)
        return response
