from typing import Any

from fastapi import Request


class AppException(Exception):
    """Base application exception with structured error envelope."""

    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int = 400,
        details: list[Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


def build_error_envelope(
    *,
    code: str,
    message: str,
    correlation_id: str,
    details: list[Any] | None = None,
) -> dict[str, Any]:
    """Build a Phase 4 compliant error response envelope."""
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
            "correlation_id": correlation_id,
        }
    }


def get_correlation_id(request: Request) -> str:
    """Extract correlation ID from request state."""
    return getattr(request.state, "correlation_id", "unknown")
