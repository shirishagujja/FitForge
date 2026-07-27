"""Settings / env loading smoke tests (no database required)."""


import pytest

from app.config import Settings, get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_cors_origins_comma_separated(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-16")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://fitforge:fitforge@localhost:5432/fitforge",
    )
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,http://localhost")

    settings = Settings()
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost"]


def test_cors_origins_json_array_string_still_works(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-16")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://fitforge:fitforge@localhost:5432/fitforge",
    )
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv(
        "CORS_ORIGINS",
        '["http://localhost:3000","http://localhost"]',
    )

    settings = Settings()
    assert settings.cors_origins == ["http://localhost:3000", "http://localhost"]


def test_database_url_from_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-16")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+asyncpg://fitforge:fitforge@db:5432/fitforge",
    )
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")
    monkeypatch.delenv("CORS_ORIGINS", raising=False)

    settings = Settings()
    assert "@db:5432" in settings.database_url
    assert settings.redis_url.startswith("redis://redis:")
