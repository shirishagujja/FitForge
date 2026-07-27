"""Integration tests for email verification and password reset."""

import re

import pytest

from app.core.email import get_sent_emails


def _extract_token_from_email(body: str) -> str:
    match = re.search(r"token=([A-Za-z0-9_\-]+)", body)
    assert match is not None, f"No token found in email body: {body}"
    return match.group(1)


@pytest.mark.asyncio
async def test_register_sends_verification_email(client, register_payload):
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201

    emails = get_sent_emails()
    assert len(emails) == 1
    assert emails[0]["to"] == "alex@example.com"
    assert "Verify" in emails[0]["subject"]
    assert "token=" in emails[0]["text_body"]


@pytest.mark.asyncio
async def test_verify_email_success(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    raw_token = _extract_token_from_email(get_sent_emails()[0]["text_body"])

    response = await client.get(f"/api/v1/auth/verify-email?token={raw_token}")
    assert response.status_code == 200
    assert response.json()["data"]["email_verified"] is True

    me_login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    access = me_login.json()["data"]["access_token"]
    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access}"})
    assert me.json()["data"]["email_verified"] is True


@pytest.mark.asyncio
async def test_verify_email_invalid_token(client):
    response = await client.get("/api/v1/auth/verify-email?token=not-a-real-token")
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


@pytest.mark.asyncio
async def test_verify_email_cannot_reuse_token(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    raw_token = _extract_token_from_email(get_sent_emails()[0]["text_body"])

    first = await client.get(f"/api/v1/auth/verify-email?token={raw_token}")
    assert first.status_code == 200

    second = await client.get(f"/api/v1/auth/verify-email?token={raw_token}")
    assert second.status_code == 400


@pytest.mark.asyncio
async def test_resend_verification(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    assert len(get_sent_emails()) == 1

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    access = login.json()["data"]["access_token"]

    resend = await client.post(
        "/api/v1/auth/resend-verification",
        headers={"Authorization": f"Bearer {access}"},
    )
    assert resend.status_code == 200
    assert len(get_sent_emails()) == 2


@pytest.mark.asyncio
async def test_forgot_and_reset_password(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)

    forgot = await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": register_payload["email"]},
    )
    assert forgot.status_code == 200
    # Generic message — no enumeration
    assert "If an account exists" in forgot.json()["message"]

    emails = get_sent_emails()
    reset_emails = [e for e in emails if "Reset" in e["subject"]]
    assert len(reset_emails) == 1
    raw_token = _extract_token_from_email(reset_emails[0]["text_body"])

    new_password = "NewSecurePass123!"
    reset = await client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": new_password,
            "password_confirm": new_password,
        },
    )
    assert reset.status_code == 200

    # Old password fails
    old_login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert old_login.status_code == 401

    # New password works
    new_login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": new_password},
    )
    assert new_login.status_code == 200


@pytest.mark.asyncio
async def test_forgot_password_unknown_email_no_enumeration(client):
    response = await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "nobody@example.com"},
    )
    assert response.status_code == 200
    assert "If an account exists" in response.json()["message"]
    # No email sent for unknown addresses
    assert get_sent_emails() == []


@pytest.mark.asyncio
async def test_reset_password_revokes_sessions(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    old_refresh = login.json()["data"]["refresh_token"]

    await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": register_payload["email"]},
    )
    raw_token = _extract_token_from_email(
        [e for e in get_sent_emails() if "Reset" in e["subject"]][0]["text_body"]
    )

    await client.post(
        "/api/v1/auth/reset-password",
        json={
            "token": raw_token,
            "password": "AnotherPass123!",
            "password_confirm": "AnotherPass123!",
        },
    )

    reuse = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert reuse.status_code == 401
