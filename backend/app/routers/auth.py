# backend/app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from backend.app.db import SessionLocal
from backend.app.models import User
from passlib.context import CryptContext
from jose import jwt
from backend.app import settings
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: int, extra: dict = None, expires_minutes: int = None):
    expires = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.settings.JWT_EXPIRES_MINUTES)
    payload = {"sub": str(subject), "exp": int(expires.timestamp())}
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.settings.JWT_SECRET, algorithm=settings.settings.JWT_ALGORITHM)
    return token

@router.post("/admin/login")
def admin_login(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.password_hash:
            raise HTTPException(status_code=401, detail="No password set")
        if not pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(user.id, extra={"type": "admin"})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()
