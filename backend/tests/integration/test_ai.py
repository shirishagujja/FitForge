"""Integration tests for the AI coach module. Real OpenAI calls cost money and can't run
reliably in CI, so every test here mocks the client — same spirit as test_email.py mocking
SMTP rather than hitting a real mail server."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.modules.ai import service as ai_service


async def _auth_headers(client, email: str, password: str = "SecurePass123!") -> dict[str, str]:
    payload = {"email": email, "password": password, "password_confirm": password}
    await client.post("/api/v1/auth/register", json=payload)
    login = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    access = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {access}"}


def _fake_completion(content: str):
    message = SimpleNamespace(content=content)
    choice = SimpleNamespace(message=message)
    return SimpleNamespace(choices=[choice])


def _mock_openai_client(monkeypatch, content: str):
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=AsyncMock(return_value=_fake_completion(content)))
        )
    )
    monkeypatch.setattr(ai_service, "_client", lambda: fake_client)
    return fake_client


@pytest.fixture
async def exercise(db_session):
    from app.modules.workouts.models import Exercise, ExerciseCategory

    squat = Exercise(name="Squat", category=ExerciseCategory.STRENGTH, muscle_group="legs")
    db_session.add(squat)
    await db_session.flush()
    await db_session.commit()
    return squat


@pytest.mark.asyncio
async def test_generate_workout_requires_auth(client):
    response = await client.post("/api/v1/ai/generate-workout", json={"goal": "build muscle"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_generate_workout_resolves_known_exercises(client, exercise, monkeypatch):
    headers = await _auth_headers(client, "ai-workout@example.com")
    llm_json = json.dumps(
        {
            "name": "Quick Leg Day",
            "exercises": [
                {"exercise_name": "Squat", "sets": 3, "reps": 10, "notes": None},
                {"exercise_name": "Unicorn Curl", "sets": 3, "reps": 12, "notes": None},
            ],
        }
    )
    _mock_openai_client(monkeypatch, llm_json)

    response = await client.post(
        "/api/v1/ai/generate-workout",
        json={"goal": "build muscle", "duration_minutes": 30, "difficulty": "beginner"},
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()["data"]
    assert body["name"] == "Quick Leg Day"
    exercises = body["exercises"]
    assert exercises[0]["exercise_name"] == "Squat"
    assert exercises[0]["exercise_id"] == str(exercise.id)
    assert exercises[1]["exercise_name"] == "Unicorn Curl"
    assert exercises[1]["exercise_id"] is None


@pytest.mark.asyncio
async def test_generate_meals_success(client, monkeypatch):
    headers = await _auth_headers(client, "ai-meals@example.com")
    llm_json = json.dumps(
        {
            "suggestions": [
                {
                    "name": "Grilled salmon bowl",
                    "estimated_calories": 520,
                    "protein_g": 40,
                    "carbs_g": 45,
                    "fat_g": 18,
                },
            ]
        }
    )
    _mock_openai_client(monkeypatch, llm_json)

    response = await client.post(
        "/api/v1/ai/generate-meals",
        json={"meal_type": "lunch", "target_calories": 500},
        headers=headers,
    )
    assert response.status_code == 200
    suggestions = response.json()["data"]["suggestions"]
    assert len(suggestions) == 1
    assert suggestions[0]["name"] == "Grilled salmon bowl"


@pytest.mark.asyncio
async def test_chat_success(client, monkeypatch):
    headers = await _auth_headers(client, "ai-chat@example.com")
    _mock_openai_client(monkeypatch, "Keep up the great work!")

    response = await client.post(
        "/api/v1/ai/chat",
        json={"messages": [{"role": "user", "content": "Any tips for today?"}]},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["data"]["message"] == "Keep up the great work!"


@pytest.mark.asyncio
async def test_chat_requires_at_least_one_message(client):
    headers = await _auth_headers(client, "ai-chat-empty@example.com")
    response = await client.post("/api/v1/ai/chat", json={"messages": []}, headers=headers)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_recommendations_success(client, monkeypatch):
    headers = await _auth_headers(client, "ai-rec@example.com")
    llm_json = json.dumps({"recommendations": ["Log a workout today!", "Stay hydrated."]})
    _mock_openai_client(monkeypatch, llm_json)

    response = await client.get("/api/v1/ai/recommendations", headers=headers)
    assert response.status_code == 200
    recs = response.json()["data"]["recommendations"]
    assert len(recs) == 2


@pytest.mark.asyncio
async def test_generate_workout_503_when_no_api_key(client, monkeypatch):
    from app.config import get_settings

    headers = await _auth_headers(client, "ai-nokey@example.com")
    monkeypatch.setattr(get_settings(), "openai_api_key", None)

    response = await client.post(
        "/api/v1/ai/generate-workout", json={"goal": "get stronger"}, headers=headers
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SERVICE_UNAVAILABLE"
