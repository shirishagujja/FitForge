"""Unit tests for password hashing and JWT helpers."""

import uuid

import pytest

from app.core.security import (
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)


def test_hash_and_verify_password():
    hashed = hash_password("SecurePass123!")
    assert hashed != "SecurePass123!"
    assert verify_password("SecurePass123!", hashed) is True
    assert verify_password("WrongPass123!", hashed) is False


def test_hash_token_is_deterministic():
    token = "refresh-token-value"
    assert hash_token(token) == hash_token(token)
    assert hash_token(token) != token


def test_access_token_roundtrip():
    user_id = uuid.uuid4()
    token, expires_in = create_access_token(
        user_id=user_id,
        role="user",
        email_verified=False,
    )
    assert expires_in == 15 * 60
    payload = decode_token(token, expected_type="access")
    assert payload["sub"] == str(user_id)
    assert payload["role"] == "user"
    assert payload["type"] == "access"


def test_refresh_token_roundtrip():
    user_id = uuid.uuid4()
    token, jti, expires_at = create_refresh_token(user_id=user_id)
    payload = decode_token(token, expected_type="refresh")
    assert payload["sub"] == str(user_id)
    assert payload["jti"] == jti
    assert payload["type"] == "refresh"
    assert expires_at is not None


def test_decode_rejects_wrong_type():
    user_id = uuid.uuid4()
    token, _ = create_access_token(user_id=user_id, role="user", email_verified=True)
    with pytest.raises(TokenError) as exc:
        decode_token(token, expected_type="refresh")
    assert exc.value.code == "UNAUTHORIZED"


def test_decode_rejects_invalid_token():
    with pytest.raises(TokenError) as exc:
        decode_token("not-a-jwt", expected_type="access")
    assert exc.value.code == "UNAUTHORIZED"
