Fintech Backend v25 - Render-ready
- Root requirements.txt exists and contains psycopg2-binary
- Absolute imports use backend.app.* (Render friendly)
- DB engine normalizes DATABASE_URL to prefer psycopg2 when unspecified
- Auto-creates initial super_admin admin@system.local / Admin@123 on first run
- Routers: /auth/login, /admin/companies, /admin/create-admin
Deployment:
1) Push this repo to GitHub (root must contain requirements.txt and backend/ folder)
2) On Render set environment variable DATABASE_URL to your Postgres URL (recommended form: postgresql+psycopg2://...)
3) Clear build cache in Render and deploy latest commit
