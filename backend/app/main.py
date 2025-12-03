from fastapi import FastAPI
from backend.app.db import init_db, ensure_first_super_admin

# IMPORT EXISTING ROUTERS
from backend.app.routers import auth, admin

# ✅ ADD THIS IMPORT
from backend.app.routers import company_auth

app = FastAPI(title="Fintech Backend v25")

# -------------------------
# Startup DB Init
# -------------------------
@app.on_event("startup")
def startup_event():
    try:
        init_db()
        ensure_first_super_admin()
    except Exception as e:
        print("Startup DB init failed:", e)

# -------------------------
# Routers
# -------------------------

# Admin Login + RBAC routes
app.include_router(auth.router, prefix="/auth")

# Admin Panel Routes
app.include_router(admin.router, prefix="/admin")

# ✅ COMPANY OTP AUTH ROUTES
app.include_router(company_auth.router, prefix="/company")

# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
