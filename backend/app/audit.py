# backend/app/audit.py
from typing import Optional, Dict, Any, List
from datetime import datetime
import json

from sqlmodel import SQLModel, Field, Session, select
from sqlalchemy import Column, Integer, String, DateTime, text
from backend.app.db import SessionLocal


class AdminAudit(SQLModel, table=True):
    """
    Records admin actions for auditing.
    Use log_admin_action(...) to create entries.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_user_id: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    action: str = Field(sa_column=Column(String, nullable=False))
    company_id: Optional[int] = Field(default=None, sa_column=Column(Integer, nullable=True))
    payload: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, nullable=False, server_default=text("now()")))


def _ensure_payload_serializable(payload: Optional[Dict[str, Any]]) -> Optional[str]:
    if payload is None:
        return None
    try:
        return json.dumps(payload)
    except Exception:
        # fallback: best-effort string
        try:
            return str(payload)
        except Exception:
            return None


def log_admin_action(db: Optional[Session] = None,
                     admin_user_id: Optional[int] = None,
                     action: str = "",
                     company_id: Optional[int] = None,
                     payload: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an admin action.

    Params:
      - db: optional SQLModel Session. If not provided a new session is created and closed.
      - admin_user_id: id of the admin user performing the action (optional)
      - action: short string describing action (required)
      - company_id: optional company context
      - payload: optional dict describing details (will be JSON-serialized)

    Usage:
      log_admin_action(db, 12, "request_company_access", 55, {"request_id": 7})
    """
    created_here = False
    if db is None:
        db = SessionLocal()
        created_here = True

    try:
        aud = AdminAudit(
            admin_user_id=admin_user_id,
            action=action,
            company_id=company_id,
            payload=_ensure_payload_serializable(payload)
        )
        db.add(aud)
        db.commit()
    except Exception:
        # do not raise in production audit to avoid breaking main flow --
        # if you want to surface errors, remove this try/except
        try:
            db.rollback()
        except Exception:
            pass
    finally:
        if created_here:
            db.close()


def query_admin_actions(limit: int = 100, company_id: Optional[int] = None, admin_user_id: Optional[int] = None) -> List[AdminAudit]:
    """
    Return recent audit entries. Filters are optional.
    """
    db = SessionLocal()
    try:
        q = select(AdminAudit).order_by(AdminAudit.created_at.desc())
        if company_id is not None:
            q = q.where(AdminAudit.company_id == company_id)
        if admin_user_id is not None:
            q = q.where(AdminAudit.admin_user_id == admin_user_id)
        if limit:
            q = q.limit(limit)
        rows = db.exec(q).all()
        return rows
    finally:
        db.close()
