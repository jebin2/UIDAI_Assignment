import logging
from logging.handlers import RotatingFileHandler

from app.core.context import request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


def setup_logging() -> None:
    from app.core.config import settings

    fmt = "%(levelname)-8s [%(request_id)s] %(name)s - %(message)s"
    formatter = logging.Formatter(fmt)
    req_filter = RequestIdFilter()

    handlers: list[logging.Handler] = []

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(req_filter)
    handlers.append(console)

    if settings.log_file_path:
        file_handler = RotatingFileHandler(
            filename=settings.log_file_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(req_filter)
        handlers.append(file_handler)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = handlers
