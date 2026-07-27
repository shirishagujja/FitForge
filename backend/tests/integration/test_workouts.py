"""Integration tests for workout CRUD and the exercise library."""

from __future__ import annotations

import pytest

from app.modules.workouts.models import Exercise, ExerciseCategory


@pytest.fixture
async def exercises(db_session):
    squat = Exercise(
        name="Squat", category=ExerciseCategory.STRENGTH, muscle_group="legs", equipment="barbell"
    )
    bench = Exercise(
        name="Bench Press",
        category=ExerciseCategory.STRENGTH,
        muscle_group="chest",
        equipment="barbell",
    )
    running = Exercise(name="Running", category=ExerciseCategory.CARDIO, muscle_group="full_body")
    db_session.add_all([squat, bench, running])
    await db_session.flush()
    await db_session.commit()
    return {"squat": squat, "bench": bench, "running": running}


async def _auth_headers(client, email: str, password: str = "SecurePass123!") -> dict[str, str]:
    payload = {"email": email, "password": password, "password_confirm": password}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    access = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access}"}


def _workout_payload(exercise_fixtures: dict, **overrides) -> dict:
    payload = {
        "name": "Leg day",
        "performed_at": "2026-07-23",
        "notes": "Felt strong",
        "exercises": [
            {
                "exercise_id": str(exercise_fixtures["squat"].id),
                "sets": 5,
                "reps": 5,
                "weight_kg": 100,
            },
        ],
    }
    payload.update(overrides)
    return payload


@pytest.mark.asyncio
async def test_list_exercises_returns_seeded(client, exercises):
    headers = await _auth_headers(client, "lister@example.com")
    response = await client.get("/api/v1/exercises", headers=headers)
    assert response.status_code == 200
    names = {e["name"] for e in response.json()["data"]}
    assert {"Squat", "Bench Press", "Running"} <= names


@pytest.mark.asyncio
async def test_list_exercises_filters_by_category(client, exercises):
    headers = await _auth_headers(client, "filter@example.com")
    response = await client.get("/api/v1/exercises?category=cardio", headers=headers)
    assert response.status_code == 200
    names = {e["name"] for e in response.json()["data"]}
    assert names == {"Running"}


@pytest.mark.asyncio
async def test_create_workout_success(client, exercises):
    headers = await _auth_headers(client, "creator@example.com")
    response = await client.post(
        "/api/v1/workouts", json=_workout_payload(exercises), headers=headers
    )
    assert response.status_code == 201
    body = response.json()["data"]
    assert body["name"] == "Leg day"
    assert len(body["exercises"]) == 1
    assert body["exercises"][0]["exercise"]["name"] == "Squat"
    assert body["exercises"][0]["sets"] == 5


@pytest.mark.asyncio
async def test_create_workout_unknown_exercise_id(client, exercises):
    headers = await _auth_headers(client, "badref@example.com")
    payload = _workout_payload(
        exercises,
        exercises=[
            {
                "exercise_id": "00000000-0000-0000-0000-000000000000",
                "sets": 3,
                "reps": 10,
            }
        ],
    )
    response = await client.post("/api/v1/workouts", json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "BAD_REQUEST"


@pytest.mark.asyncio
async def test_list_workouts_returns_summaries(client, exercises):
    headers = await _auth_headers(client, "history@example.com")
    await client.post("/api/v1/workouts", json=_workout_payload(exercises), headers=headers)

    response = await client.get("/api/v1/workouts", headers=headers)
    assert response.status_code == 200
    summaries = response.json()["data"]
    assert len(summaries) == 1
    assert summaries[0]["exercise_count"] == 1
    assert summaries[0]["name"] == "Leg day"


@pytest.mark.asyncio
async def test_get_workout_not_found(client, exercises):
    headers = await _auth_headers(client, "missing@example.com")
    response = await client.get(
        "/api/v1/workouts/00000000-0000-0000-0000-000000000000", headers=headers
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_workout(client, exercises):
    headers = await _auth_headers(client, "editor@example.com")
    create = await client.post(
        "/api/v1/workouts", json=_workout_payload(exercises), headers=headers
    )
    workout_id = create.json()["data"]["id"]

    updated_payload = _workout_payload(
        exercises,
        name="Leg day (heavier)",
        exercises=[
            {"exercise_id": str(exercises["squat"].id), "sets": 3, "reps": 3, "weight_kg": 120},
            {"exercise_id": str(exercises["bench"].id), "sets": 4, "reps": 8, "weight_kg": 60},
        ],
    )
    response = await client.put(
        f"/api/v1/workouts/{workout_id}", json=updated_payload, headers=headers
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["name"] == "Leg day (heavier)"
    assert len(body["exercises"]) == 2


@pytest.mark.asyncio
async def test_delete_workout(client, exercises):
    headers = await _auth_headers(client, "deleter@example.com")
    create = await client.post(
        "/api/v1/workouts", json=_workout_payload(exercises), headers=headers
    )
    workout_id = create.json()["data"]["id"]

    delete_response = await client.delete(f"/api/v1/workouts/{workout_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/workouts/{workout_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_workout_ownership_enforced(client, exercises):
    owner_headers = await _auth_headers(client, "owner@example.com")
    other_headers = await _auth_headers(client, "intruder@example.com")

    create = await client.post(
        "/api/v1/workouts", json=_workout_payload(exercises), headers=owner_headers
    )
    workout_id = create.json()["data"]["id"]

    get_response = await client.get(f"/api/v1/workouts/{workout_id}", headers=other_headers)
    assert get_response.status_code == 404

    put_response = await client.put(
        f"/api/v1/workouts/{workout_id}",
        json=_workout_payload(exercises),
        headers=other_headers,
    )
    assert put_response.status_code == 404

    delete_response = await client.delete(
        f"/api/v1/workouts/{workout_id}", headers=other_headers
    )
    assert delete_response.status_code == 404
