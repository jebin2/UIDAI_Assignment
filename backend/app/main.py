from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.routes import router
from app.api.exception_handlers import register_exception_handlers
from app.middleware.access_log import AccessLogMiddleware
from app.middleware.rate_limit.middleware import RateLimitMiddleware

setup_logging()

app = FastAPI(title="UIDAI Sandbox - Secure Payload API", version="1.0.0")

# Middleware - registered in reverse execution order
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.add_middleware(AccessLogMiddleware)

# Exception handlers
register_exception_handlers(app)

# Routes
app.include_router(router)
