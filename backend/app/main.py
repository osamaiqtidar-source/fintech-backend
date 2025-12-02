# backend/app/main.py

from fastapi import FastAPI
from backend.app.db import init_db, ensure_first_super_admin
from backend.app.routers import auth, admin

app = FastAPI(title="Fintech Backend v25")

# Run DB initialization ONLY when FastAPI is fully ready
@app.on_event("startup")
def startup_event():
    try:
        init_db()
        ensure_first_super_admin()
    except Exception as e:
        print("Startup DB init failed:", e)

# include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin")

@app.get("/health")
def health():
    return {"status": "ok"}
