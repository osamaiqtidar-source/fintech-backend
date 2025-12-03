# backend/app/routers/admin.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from backend.app.deps import get_current_actor
from backend.app.db import SessionLocal
from backend.app.models_admin_access import AdminCompanyAccess
from backend.app.audit import log_admin_action
from backend.app.utils import generate_otp, send_otp_to_company_contact

from datetime import datetime, timedelta

router = APIRouter()

@router.post("/company/{company_id}/request-access")
def request_company_access(company_id: int, actor = Depends(get_current_actor), background_tasks: BackgroundTasks = None):
    """
    Admin requests access to a company. Generates OTP and sends to company owner.
    """
    if actor["type"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin users can request access")
    admin_user = actor["user"]
    db = SessionLocal()
    try:
        otp = generate_otp()
        expires = datetime.utcnow() + timedelta(minutes=10)
        req = AdminCompanyAccess(admin_id=admin_user.id, company_id=company_id, otp=otp, expires_at=expires)
        db.add(req); db.commit(); db.refresh(req)

        if background_tasks is not None:
            background_tasks.add_task(send_otp_to_company_contact, company_id, otp)
        else:
            try:
                send_otp_to_company_contact(company_id, otp)
            except Exception:
                pass

        log_admin_action(db, admin_user.id, "request_company_access", company_id, {"request_id": req.id})
        return {"ok": True, "request_id": req.id, "message": "OTP sent to company owner"}
    finally:
        db.close()
