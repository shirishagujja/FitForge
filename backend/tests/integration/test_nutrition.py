"""Integration tests for meals, water entries, and the daily nutrition summary."""

from __future__ import annotations

import pytest


async def _auth_headers(client, email: str, password: str = "SecurePass123!") -> dict[str, str]:
    payload = {"email": email, "password": password, "password_confirm": password}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    access = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access}"}


def _meal_payload(**overrides) -> dict:
    payload = {
        "name": "Chicken salad",
        "logged_at": "2026-07-23",
        "calories": 450,
        "protein_g": 40,
        "carbs_g": 20,
        "fat_g": 15,
        "notes": None,
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_create_meal_success(client):
    headers = await _auth_headers(client, "meal-creator@example.com")
    response = await client.post("/api/v1/meals", json=_meal_payload(), headers=headers)
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["name"] == "Chicken salad"
    assert body["calories"] == 450


@pytest.mark.asyncio
async def test_list_meals_filters_by_date(client):
    headers = await _auth_headers(client, "meal-lister@example.com")
    await client.post("/api/v1/meals", json=_meal_payload(logged_at="2026-07-20"), headers=headers)
    await client.post("/api/v1/meals", json=_meal_payload(logged_at="2026-07-23"), headers=headers)

    response = await client.get(
        "/api/v1/meals?date_from=2026-07-23&date_to=2026-07-23", headers=headers
    )
    assert response.status_code == 200
    meals = response.json()["data"]
    assert len(meals) == 1
    assert meals[0]["logged_at"] == "2026-07-23"


@pytest.mark.asyncio
async def test_update_and_delete_meal(client):
    headers = await _auth_headers(client, "meal-editor@example.com")
    create = await client.post("/api/v1/meals", json=_meal_payload(), headers=headers)
    meal_id = create.json()["data"]["id"]

    update = await client.put(
        f"/api/v1/meals/{meal_id}", json=_meal_payload(calories=600), headers=headers
    )
    assert update.status_code == 200
    assert update.json()["data"]["calories"] == 600

    delete = await client.delete(f"/api/v1/meals/{meal_id}", headers=headers)
    assert delete.status_code == 204

    get_response = await client.get(f"/api/v1/meals/{meal_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_meal_ownership_enforced(client):
    owner_headers = await _auth_headers(client, "meal-owner@example.com")
    other_headers = await _auth_headers(client, "meal-intruder@example.com")

    create = await client.post("/api/v1/meals", json=_meal_payload(), headers=owner_headers)
    meal_id = create.json()["data"]["id"]

    response = await client.get(f"/api/v1/meals/{meal_id}", headers=other_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_water_entry_create_and_list(client):
    headers = await _auth_headers(client, "water-user@example.com")
    await client.post(
        "/api/v1/water-entries",
        json={"logged_at": "2026-07-23", "amount_ml": 250},
        headers=headers,
    )
    await client.post(
        "/api/v1/water-entries",
        json={"logged_at": "2026-07-23", "amount_ml": 500},
        headers=headers,
    )

    response = await client.get("/api/v1/water-entries?date=2026-07-23", headers=headers)
    assert response.status_code == 200
    entries = response.json()["data"]
    assert len(entries) == 2
    assert {e["amount_ml"] for e in entries} == {250, 500}


@pytest.mark.asyncio
async def test_daily_summary_aggregates_meals_and_water(client):
    headers = await _auth_headers(client, "summary-user@example.com")
    await client.post(
        "/api/v1/meals",
        json=_meal_payload(name="Breakfast", calories=300, protein_g=20, carbs_g=30, fat_g=10),
        headers=headers,
    )
    await client.post(
        "/api/v1/meals",
        json=_meal_payload(name="Lunch", calories=500, protein_g=35, carbs_g=40, fat_g=15),
        headers=headers,
    )
    await client.post(
        "/api/v1/water-entries",
        json={"logged_at": "2026-07-23", "amount_ml": 750},
        headers=headers,
    )

    response = await client.get("/api/v1/nutrition/summary?date=2026-07-23", headers=headers)
    assert response.status_code == 200
    summary = response.json()["data"]
    assert summary["total_calories"] == 800
    assert summary["total_protein_g"] == 55
    assert summary["total_carbs_g"] == 70
    assert summary["total_fat_g"] == 25
    assert summary["total_water_ml"] == 750


@pytest.mark.asyncio
async def test_daily_summary_zero_when_no_entries(client):
    headers = await _auth_headers(client, "empty-summary@example.com")
    response = await client.get("/api/v1/nutrition/summary?date=2026-07-23", headers=headers)
    assert response.status_code == 200
    summary = response.json()["data"]
    assert summary["total_calories"] == 0
    assert summary["total_water_ml"] == 0
