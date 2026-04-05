import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.crypto_service import DecryptionError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DecryptionError)
    async def decryption_error_handler(_: Request, exc: DecryptionError) -> JSONResponse:
        logger.warning("DECRYPTION_FAILED", exc_info=exc)
        return JSONResponse(
            status_code=400,
            content={"error": "decryption_failed", "message": "We could not verify your submission. Please try again."},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
        logger.warning("INVALID_PAYLOAD", exc_info=exc)
        return JSONResponse(
            status_code=422,
            content={"error": "invalid_payload", "message": "Your submission is incomplete or incorrectly formatted. Please check your details and try again."},
        )
