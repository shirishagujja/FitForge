"""Integration tests for auth register/login/refresh/logout/me."""

import pytest


@pytest.mark.asyncio
async def test_register_success(client, register_payload):
    response = await client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["email"] == "alex@example.com"
    assert body["data"]["email_verified"] is False
    assert body["data"]["role"] == "user"
    assert "message" in body


@pytest.mark.asyncio
async def test_register_duplicate_email(client, register_payload):
    first = await client.post("/api/v1/auth/register", json=register_payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/auth/register", json=register_payload)
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "CONFLICT"


@pytest.mark.asyncio
async def test_register_weak_password(client, register_payload):
    payload = {**register_payload, "password": "weak", "password_confirm": "weak"}
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_login_and_me(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert login.status_code == 200
    tokens = login.json()["data"]
    assert tokens["token_type"] == "bearer"
    assert tokens["expires_in"] == 900
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    me = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "alex@example.com"
    assert me.json()["data"]["has_profile"] is False


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": "WrongPass123!"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


@pytest.mark.asyncio
async def test_refresh_rotates_tokens(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    old_refresh = login.json()["data"]["refresh_token"]

    refreshed = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert refreshed.status_code == 200
    new_refresh = refreshed.json()["data"]["refresh_token"]
    assert new_refresh != old_refresh

    # Old refresh token should be rejected (reuse detection / revoked)
    reuse = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert reuse.status_code == 401


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client, register_payload):
    await client.post("/api/v1/auth/register", json=register_payload)
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    refresh_token = login.json()["data"]["refresh_token"]

    logout = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
    )
    assert logout.status_code == 200

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_auth(client):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"
