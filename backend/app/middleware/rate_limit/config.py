"""
Rate limit rules per route.

Each entry:
  "METHOD /path" -> { "capacity": int, "window_seconds": int }

"""

from app.core.config import settings

RATE_LIMIT_RULES: dict[str, dict] = {
    "POST /api/v1/sandbox/secure-payload": {
        "capacity": settings.rate_limit_capacity,
        "window_seconds": settings.rate_limit_window_seconds,
    },
}
