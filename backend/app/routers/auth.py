from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.app.db import SessionLocal
from backend.app.models import User
from passlib.context import CryptContext
from jose import jwt
try:
    from backend.app.settings import settings
except Exception:
    class settings:
        JWT_SECRET = 'CHANGE_ME'
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter()

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post('/login')
def login(payload: LoginSchema):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user or not pwd_context.verify(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail='Invalid credentials')
        token = jwt.encode({'sub': str(user.id)}, settings.JWT_SECRET, algorithm='HS256')
        return {'access_token': token, 'token_type': 'bearer'}
    finally:
        db.close()
