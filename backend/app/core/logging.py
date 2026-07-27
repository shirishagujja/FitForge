import logging
import sys
from typing import Any

from app.config import get_settings

settings = get_settings()


def configure_logging() -> None:
    """Configure structured application logging."""
    log_level = logging.DEBUG if settings.environment == "development" else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_extra(**kwargs: Any) -> dict[str, Any]:
    """Helper for structured log context."""
    return kwargs
