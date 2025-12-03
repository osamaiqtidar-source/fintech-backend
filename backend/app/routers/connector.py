# backend/app/routers/connector.py
from fastapi import APIRouter, Header, HTTPException, Depends
from backend.app.db import SessionLocal
from backend.app import settings
from backend.app import models
from backend.app.audit import log_admin_action
import os

router = APIRouter()
CONNECTOR_API_KEY = os.getenv("CONNECTOR_API_KEY", settings.settings.CONNECTOR_API_KEY)

@router.post("/register")
def register_agent(op: dict, x_connector_key: str = Header(None)):
    if x_connector_key != CONNECTOR_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid connector key")
    # registration logic (as you had)
    return {"ok": True}

@router.post("/sync")
def sync(op: dict, x_connector_key: str = Header(None)):
    if x_connector_key != CONNECTOR_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid connector key")

    db = SessionLocal()
    try:
        sop = models.SyncOperation(
            company_id = op.get("company_id", 0),
            source = op.get("source", "connector"),
            operation_type = op.get("type", "sync"),
            payload = op.get("payload")
        )
        db.add(sop); db.commit(); db.refresh(sop)
        return {"ok": True, "sync_id": sop.id}
    finally:
        db.close()
