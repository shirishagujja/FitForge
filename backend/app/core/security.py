"""Password hashing and JWT token utilities."""

from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.config import get_settings

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a password with Argon2id."""
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against an Argon2 hash."""
    try:
        return _password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def hash_token(token: str) -> str:
    """Hash a refresh token for storage (never store raw tokens)."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(
    *,
    user_id: uuid.UUID,
    role: str,
    email_verified: bool,
) -> tuple[str, int]:
    """Create a short-lived access JWT. Returns (token, expires_in_seconds)."""
    settings = get_settings()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expires_in = int(expires_delta.total_seconds())
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "email_verified": email_verified,
        "type": "access",
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + expires_delta,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token, expires_in


def create_refresh_token(*, user_id: uuid.UUID) -> tuple[str, str, datetime]:
    """Create a refresh JWT.

    Returns (raw_token, jti, expires_at).
    Store only the hash of raw_token; jti is the DB primary key.
    """
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
    jti = str(uuid.uuid4())
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": jti,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token, jti, expires_at


def decode_token(token: str, *, expected_type: str) -> dict[str, Any]:
    """Decode and validate a JWT, ensuring the token type matches."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenError("TOKEN_EXPIRED", "Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise TokenError("UNAUTHORIZED", "Invalid token") from exc

    if payload.get("type") != expected_type:
        raise TokenError("UNAUTHORIZED", "Invalid token type")

    return payload


def generate_secure_token(nbytes: int = 32) -> str:
    """Generate a URL-safe random token (email verify / password reset)."""
    return secrets.token_urlsafe(nbytes)


class TokenError(Exception):
    """Raised when JWT validation fails."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)
