"""Integration tests for body measurements and goals."""

from __future__ import annotations

import pytest


async def _auth_headers(client, email: str, password: str = "SecurePass123!") -> dict[str, str]:
    payload = {"email": email, "password": password, "password_confirm": password}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    access = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access}"}


def _measurement_payload(**overrides) -> dict:
    payload = {"recorded_at": "2026-07-23", "weight_kg": 80.5, "body_fat_pct": 18.2}
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_create_measurement_success(client):
    headers = await _auth_headers(client, "measure-creator@example.com")
    response = await client.post(
        "/api/v1/measurements", json=_measurement_payload(), headers=headers
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["weight_kg"] == 80.5


@pytest.mark.asyncio
async def test_create_measurement_upserts_same_day(client):
    headers = await _auth_headers(client, "measure-upsert@example.com")
    first = await client.post(
        "/api/v1/measurements", json=_measurement_payload(weight_kg=80.0), headers=headers
    )
    second = await client.post(
        "/api/v1/measurements", json=_measurement_payload(weight_kg=79.5), headers=headers
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["data"]["id"] == second.json()["data"]["id"]
    assert second.json()["data"]["weight_kg"] == 79.5

    listing = await client.get("/api/v1/measurements", headers=headers)
    assert len(listing.json()["data"]) == 1


@pytest.mark.asyncio
async def test_update_and_delete_measurement(client):
    headers = await _auth_headers(client, "measure-editor@example.com")
    create = await client.post(
        "/api/v1/measurements", json=_measurement_payload(), headers=headers
    )
    measurement_id = create.json()["data"]["id"]

    update = await client.put(
        f"/api/v1/measurements/{measurement_id}",
        json=_measurement_payload(weight_kg=78.0),
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["data"]["weight_kg"] == 78.0

    delete = await client.delete(f"/api/v1/measurements/{measurement_id}", headers=headers)
    assert delete.status_code == 204

    get_response = await client.get(f"/api/v1/measurements/{measurement_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_measurement_ownership_enforced(client):
    owner_headers = await _auth_headers(client, "measure-owner@example.com")
    other_headers = await _auth_headers(client, "measure-intruder@example.com")

    create = await client.post(
        "/api/v1/measurements", json=_measurement_payload(), headers=owner_headers
    )
    measurement_id = create.json()["data"]["id"]

    response = await client.get(f"/api/v1/measurements/{measurement_id}", headers=other_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_goal_create_update_mark_achieved(client):
    headers = await _auth_headers(client, "goal-user@example.com")
    create = await client.post(
        "/api/v1/goals",
        json={"title": "Reach 75kg", "target_weight_kg": 75, "target_date": "2026-12-31"},
        headers=headers,
    )
    assert create.status_code == 201
    goal_id = create.json()["data"]["id"]
    assert create.json()["data"]["status"] == "active"

    update = await client.put(
        f"/api/v1/goals/{goal_id}",
        json={
            "title": "Reach 75kg",
            "target_weight_kg": 75,
            "target_date": "2026-12-31",
            "status": "achieved",
        },
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "achieved"


@pytest.mark.asyncio
async def test_goal_ownership_enforced(client):
    owner_headers = await _auth_headers(client, "goal-owner@example.com")
    other_headers = await _auth_headers(client, "goal-intruder@example.com")

    create = await client.post(
        "/api/v1/goals", json={"title": "Bench 100kg"}, headers=owner_headers
    )
    goal_id = create.json()["data"]["id"]

    delete_response = await client.delete(f"/api/v1/goals/{goal_id}", headers=other_headers)
    assert delete_response.status_code == 404
