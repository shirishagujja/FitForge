# FitForge

AI-Powered Fitness Platform — Phase 5 scaffolding.

## Stack

- **Backend:** FastAPI, SQLAlchemy 2.0 (async), Alembic, Celery, Redis, PostgreSQL 16
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui placeholders
- **Infra:** Docker Compose, nginx reverse proxy
- **CI:** GitHub Actions (lint, test, build)

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url> fitforge
cd fitforge
cp .env.example .env
```

Edit `.env` and set a secure `SECRET_KEY`.

### 2. Run with Docker Compose

```bash
docker compose up --build
```

Services:

| Service  | Description              |
|----------|--------------------------|
| nginx    | http://localhost (port 80) |
| api      | FastAPI backend          |
| frontend | Next.js app              |
| worker   | Celery worker            |
| beat     | Celery beat scheduler    |
| db       | PostgreSQL 16            |
| redis    | Redis 7                  |

### 3. Verify

- Frontend: http://localhost
- Health: http://localhost/api/v1/health
- Readiness: http://localhost/api/v1/ready
- API docs (dev): http://localhost/api/docs
- Mailhog UI: http://localhost:8025

### Environment notes

| Context | `DATABASE_URL` host | `REDIS_URL` host |
|---------|---------------------|------------------|
| Docker Compose | `db` (forced in compose `environment:`) | `redis` |
| Local pytest / uvicorn | `localhost` (`backend/.env` or `tests/conftest.py`) | `localhost` |

`CORS_ORIGINS` must be **comma-separated**, not JSON:
`CORS_ORIGINS=http://localhost:3000,http://localhost`

## Local Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Ensure PostgreSQL and Redis are running (docker compose up -d db redis), then:
export DATABASE_URL=postgresql+asyncpg://fitforge:fitforge@localhost:5432/fitforge
export REDIS_URL=redis://localhost:6379/0
export SECRET_KEY=dev-secret-key-change-me
export ENVIRONMENT=development

alembic upgrade head
uvicorn app.main:app --reload --port 8000
pytest -v
ruff check .
```

### Auth smoke test (after API is up)

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@example.com","password":"SecurePass123!","password_confirm":"SecurePass123!"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@example.com","password":"SecurePass123!"}'

# Me (replace TOKEN)
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TOKEN"
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api` for direct API access during local dev.

## Project Structure

```
fitforge/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── nginx/            # Reverse proxy config
├── .github/workflows # CI pipelines
└── docker-compose.yml
```

## License

Proprietary — FitForge
