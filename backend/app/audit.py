# backend/app/audit.py
from backend.app.db import SessionLocal
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, String, DateTime, func
from typing import Optional
import json

# Lightweight audit model (if you prefer separate file define SQLModel; here we use raw insertion)
def log_admin_action(db, admin_user_id: int, action: str, company_id: Optional[int] = None, payload: Optional[dict] = None):
    """
    If db session provided, use it; else create temporary session.
    """
    created_here = False
    if db is None:
        db = SessionLocal()
        created_here = True
    try:
        # Using simple table 'adminaudit' (created by migration). Insert record.
        payload_json = None
        try:
            payload_json = json.dumps(payload) if payload is not None else None
        except Exception:
            payload_json = None
        sql = """
        INSERT INTO adminaudit (admin_user_id, action, company_id, payload)
        VALUES (:admin_user_id, :action, :company_id, :payload)
        """
        db.execute(sql, {"admin_user_id": admin_user_id, "action": action, "company_id": company_id, "payload": payload_json})
        db.commit()
    finally:
        if created_here:
            db.close()
