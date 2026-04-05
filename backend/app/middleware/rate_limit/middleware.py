import json
import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.rate_limit.config import RATE_LIMIT_RULES
from app.cache.redis_mock import cache

logger = logging.getLogger(__name__)


def _window_key(route_key: str, partner_id: str) -> str:
    return f"rate_limit:{route_key}:{partner_id}"


def _check_sliding_window(partner_id: str, route_key: str, rule: dict) -> bool:
    """
    Sliding Window rate limiter.
    """
    capacity: int = rule["capacity"]
    window_seconds: int = rule["window_seconds"]
    key = _window_key(route_key, partner_id)
    now = time.monotonic()
    window_start = now - window_seconds
    allowed = False

    def update(current: list) -> list:
        nonlocal allowed
        timestamps = [t for t in (current or []) if t > window_start]
        if len(timestamps) < capacity:
            timestamps.append(now)
            allowed = True
        return timestamps

    final = cache.get_and_set(key, update)

    if not allowed:
        logger.warning(
            "RATE_LIMIT_EXCEEDED route=%s partner_id=%s count=%s capacity=%s",
            route_key, partner_id, len(final), capacity,
        )
        return False

    logger.info(
        "RATE_LIMIT_ALLOWED route=%s partner_id=%s count=%s capacity=%s",
        route_key, partner_id, len(final), capacity,
    )
    return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        route_key = f"{request.method} {request.url.path}"

        rule = RATE_LIMIT_RULES.get(route_key)
        if rule is None:
            return await call_next(request)

        body_bytes = await request.body()
        try:
            body = json.loads(body_bytes)
            partner_id = body.get("partner_id", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return JSONResponse(status_code=400, content={"error": "invalid_json", "message": "Request body must be valid JSON"})

        if not partner_id:
            return JSONResponse(status_code=400, content={"error": "missing_field", "message": "partner_id is required"})

        if not _check_sliding_window(partner_id, route_key, rule):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "You are submitting too quickly. Please wait a moment and try again.",
                },
                headers={"Retry-After": str(rule["window_seconds"])},
            )

        return await call_next(request)
