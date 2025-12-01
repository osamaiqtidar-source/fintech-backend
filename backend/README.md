Backend README - Production-ready scaffold

1. Copy .env.example to .env and edit DATABASE_URL, SECRET_KEY, CONNECTOR_API_KEY, SMTP_* and CELERY settings.
2. Build & run with docker compose:
   docker compose up --build
3. Run migrations:
   docker compose exec backend alembic upgrade head
4. Create admin user:
   # Use the users.create endpoint or psql to insert admin user
5. Start worker (in docker-compose worker service will run Celery)
