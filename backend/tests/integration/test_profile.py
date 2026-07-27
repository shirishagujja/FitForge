"""Integration tests for the profile module (single-row-per-user upsert)."""

from __future__ import annotations

import pytest


async def _auth_headers(client, email: str, password: str = "SecurePass123!") -> dict[str, str]:
    payload = {"email": email, "password": password, "password_confirm": password}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    access = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access}"}


@pytest.mark.asyncio
async def test_get_profile_404_when_none_exists(client):
    headers = await _auth_headers(client, "profile-none@example.com")
    response = await client.get("/api/v1/profile", headers=headers)
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_me_has_profile_false_before_creation(client):
    headers = await _auth_headers(client, "profile-hasprofile@example.com")
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["has_profile"] is False


@pytest.mark.asyncio
async def test_create_profile_via_put(client):
    headers = await _auth_headers(client, "profile-create@example.com")
    payload = {
        "display_name": "Alex",
        "date_of_birth": "1995-06-15",
        "sex": "female",
        "height_cm": 168.5,
        "fitness_goal": "Build strength",
        "activity_level": "moderate",
    }
    response = await client.put("/api/v1/profile", json=payload, headers=headers)
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["display_name"] == "Alex"
    assert body["height_cm"] == 168.5

    get_response = await client.get("/api/v1/profile", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["data"]["display_name"] == "Alex"


@pytest.mark.asyncio
async def test_me_has_profile_true_after_creation(client):
    headers = await _auth_headers(client, "profile-hasprofile2@example.com")
    await client.put(
        "/api/v1/profile", json={"display_name": "Sam"}, headers=headers
    )
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["has_profile"] is True


@pytest.mark.asyncio
async def test_update_profile_upserts_not_duplicates(client):
    headers = await _auth_headers(client, "profile-upsert@example.com")
    first = await client.put(
        "/api/v1/profile", json={"display_name": "First Name"}, headers=headers
    )
    second = await client.put(
        "/api/v1/profile", json={"display_name": "Updated Name"}, headers=headers
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["data"]["id"] == second.json()["data"]["id"]
    assert second.json()["data"]["display_name"] == "Updated Name"

    get_response = await client.get("/api/v1/profile", headers=headers)
    assert get_response.json()["data"]["display_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_profile_requires_auth(client):
    response = await client.get("/api/v1/profile")
    assert response.status_code == 401
