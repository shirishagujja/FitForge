"""Unit tests for email builders."""

from app.core.email import build_password_reset_email, build_verification_email


def test_verification_email_contains_token_link():
    payload = build_verification_email("alex@example.com", "abc123token")
    assert payload.to_email == "alex@example.com"
    assert "abc123token" in payload.text_body
    assert "verify-email?token=abc123token" in payload.text_body


def test_password_reset_email_contains_token_link():
    payload = build_password_reset_email("alex@example.com", "reset456")
    assert "reset-password?token=reset456" in payload.text_body
    assert "Reset" in payload.subject
