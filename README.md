# Full Production Fintech Backend (FastAPI)

This repository is a production-oriented scaffold for the Fintech Connector backend.
It includes:
- FastAPI app with JWT auth, user & admin management
- Sync operations queue, connector endpoints, subscription system
- App update endpoints for mobile clients
- Alembic migrations configured
- Celery + Redis for background jobs (reminders, expiry)
- SMTP reminder wiring & example
- Dockerfile, docker-compose for local dev
- Render deployment notes

**Important**
- Replace secret values in .env before production.
- Review and secure connector API keys and admin accounts.
