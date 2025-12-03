# backend/app/routers/company_auth.py
from fastapi import APIRouter, HTTPException
from backend.app.db import SessionLocal
from backend.app.models_company import Company
from backend.app.models_admin_access import AdminCompanyAccess
from datetime import datetime, timedelta
from jose import jwt
from backend.app import settings
from backend.app.audit import log_admin_action

router = APIRouter()

@router.post("/access-approve")
def approve_access(phone: str, otp: str):
    """
    Company owner calls this with their phone and the OTP they received.
    Approves the admin access request and issues a temporary admin_company_access token.
    """
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.phone == phone).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        req = db.query(AdminCompanyAccess).filter(
            AdminCompanyAccess.company_id == company.id,
            AdminCompanyAccess.otp == otp,
            AdminCompanyAccess.expires_at > datetime.utcnow(),
            AdminCompanyAccess.approved == False
        ).first()

        if not req:
            raise HTTPException(status_code=401, detail="Invalid or expired OTP")

        req.approved = True
        db.add(req); db.commit()

        payload = {
            "sub": str(req.admin_id),
            "company_id": req.company_id,
            "type": "admin_company_access",
            "exp": int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        }
        token = jwt.encode(payload, settings.settings.JWT_SECRET, algorithm=settings.settings.JWT_ALGORITHM)

        log_admin_action(db, req.admin_id, "approve_company_access", req.company_id, {"request_id": req.id})
        return {"ok": True, "access_token": token, "expires_in": 600}
    finally:
        db.close()
