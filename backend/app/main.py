# backend/app/main.py
from fastapi import FastAPI
from backend.app.db import init_db, ensure_first_super_admin
from backend.app.routers import auth, admin, company_auth, connector, invoices, einvoice
from backend.app.export.routes import export_router
#from backend.app.tasks import start_backup_scheduler

app = FastAPI(title="Fintech Backend")

@app.on_event("startup")
def startup_event():
    init_db()
    ensure_first_super_admin()
    # start backup scheduler if you enabled and configured S3 credentials
    # start_backup_scheduler()

app.include_router(auth.router, prefix="/auth")
app.include_router(admin.router, prefix="/admin")
app.include_router(company_auth.router, prefix="/company")
app.include_router(connector.router, prefix="/connector")
app.include_router(invoices.router, prefix="/invoices")
app.include_router(einvoice.router, prefix="/einvoice")
app.include_router(export_router, prefix="/export", tags=["export"])

@app.get("/health")
def health():
    return {"status": "ok"}
