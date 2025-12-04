from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import random
import string

from backend.app.db import SessionLocal
from backend.app.company import Company
from backend.app.settings import settings
from jose import jwt

from backend.app.utils.otp_delivery import send_sms_otp, send_email_otp
from backend.app.deps import get_current_actor  # ⭐ ADDED

router = APIRouter(prefix="/company", tags=["company-auth"])

OTP_TTL_MINUTES = 5
JWT_TTL_MINUTES = 60 * 24 * 7   # 7 days

class RequestOtp(BaseModel):
    phone: str
    email: str | None = None
    name: str | None = None

class VerifyOtp(BaseModel):
    phone: str
    otp: str


def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))


def issue_company_token(company_id: int):
    exp = datetime.utcnow() + timedelta(minutes=JWT_TTL_MINUTES)
    return jwt.encode(
        {
            "sub": str(company_id),
            "type": "company",
            "exp": int(exp.timestamp())
        },
        settings.JWT_SECRET,
        algorithm="HS256"
    )


@router.post("/request-otp")
def request_otp(payload: RequestOtp, background: BackgroundTasks):
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.phone == payload.phone).first()

        # Auto-register company if first time
        if not company:
            company = Company(
                phone=payload.phone,
                email=payload.email,
                name=payload.name or payload.phone,
            )
            try:
                db.add(company)
                db.commit()
                db.refresh(company)
            except IntegrityError:
                db.rollback()
                company = db.query(Company).filter(Company.phone == payload.phone).first()

        otp = generate_otp()
        expires = datetime.utcnow() + timedelta(minutes=OTP_TTL_MINUTES)

        company.otp_code = otp
        company.otp_expires_at = expires

        db.add(company)
        db.commit()

        # Deliver OTP via SMS + Email
        background.add_task(send_sms_otp, company.phone, otp)
        if company.email:
            background.add_task(send_email_otp, company.email, otp)

        return {"ok": True, "expires_at": expires.isoformat()}
    finally:
        db.close()


@router.post("/verify-otp")
def verify_otp(payload: VerifyOtp):
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.phone == payload.phone).first()
        if not company:
            raise HTTPException(404, "Company not found")

        if not company.otp_code or not company.otp_expires_at:
            raise HTTPException(400, "OTP not requested")

        if datetime.utcnow() > company.otp_expires_at:
            company.otp_code = None
            company.otp_expires_at = None
            db.commit()
            raise HTTPException(400, "OTP expired")

        if payload.otp != company.otp_code:
            raise HTTPException(401, "Invalid OTP")

        # OTP verified – clear OTP
        company.otp_code = None
        company.otp_expires_at = None
        db.commit()

        token = issue_company_token(company.id)
        return {"access_token": token, "token_type": "bearer", "company_id": company.id}
    finally:
        db.close()


@router.post("/logout")
def logout():
    return {"ok": True}


@router.patch("/settings/language")
def update_language(data: dict, actor=Depends(get_current_actor)):
    if actor['type'] != 'company':
        raise HTTPException(status_code=403, detail="Only company user can change language")
    lang = data.get("language")
    if not lang:
        raise HTTPException(status_code=400, detail="language required")
    db=SessionLocal()
    try:
        db.execute("UPDATE company SET language=%s WHERE id=%s",(lang,actor['company'].id))
        db.commit()
        return {"ok":True,"language":lang}
    finally:
        db.close()
