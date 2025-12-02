Backend v16 patch notes
- requirements.txt updated to include:
    sqlmodel==0.0.17
    SQLAlchemy==2.0.31
    psycopg[binary]
- backend/app/deps.py added with role helpers (require_admin, require_super_admin, etc.)
- backend/app/db.py injected with auto-create first super_admin (admin@system.local / Admin@123)
- .env.example updated to use postgresql+psycopg:// prefix
- Staff and Viewer cannot view or edit system API settings; only admin & super_admin can view/edit
- To deploy on Render:
    1) Push this repo to GitHub
    2) Ensure DATABASE_URL uses postgresql+psycopg://...
    3) Clear build cache and deploy
    4) After first run, login with admin@system.local / Admin@123 and change password
