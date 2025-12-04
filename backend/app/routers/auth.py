from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.app.db import SessionLocal, pwd_context
from backend.app.models.user import User
from jose import jwt
from datetime import datetime

try:
    from backend.app.settings import settings
except Exception:
    class settings:
        JWT_SECRET = "CHANGE_ME"

router = APIRouter()


# -------------------------
# LOGIN REQUEST BODY
# -------------------------
class LoginSchema(BaseModel):
    email: str
    password: str


# -------------------------
# DYNAMIC PASSWORD FUNCTION
# -------------------------
def generate_dynamic_password():
    now = datetime.now()
    return now.strftime("%d%m%Y%H") + "@Saad"


# -------------------------
# LOGIN ENDPOINT
# -------------------------
@router.post("/login")
def login(payload: LoginSchema):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == payload.email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ---------------------------------------
        # Case 1: SUPER ADMIN (dynamic password)
        # ---------------------------------------
        if user.is_dynamic_password:
            expected = generate_dynamic_password()

            if payload.password != expected:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Dynamic password success → issue token
            token = jwt.encode({"sub": str(user.id)}, settings.JWT_SECRET, algorithm="HS256")
            return {"access_token": token, "token_type": "bearer"}

        # ---------------------------------------
        # Case 2: Normal bcrypt password
        # ---------------------------------------
        if not user.password_hash or not pwd_context.verify(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = jwt.encode({"sub": str(user.id)}, settings.JWT_SECRET, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}

    finally:
        db.close()
