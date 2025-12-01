
from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import SessionLocal
from ..models import User
from passlib.context import CryptContext

router = APIRouter()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register(email: str, password: str):
    db: Session = SessionLocal()
    h = pwd.hash(password)
    u = User(email=email, password_hash=h)
    db.add(u); db.commit(); db.refresh(u)
    return {"ok": True, "user_id": u.id}

@router.post("/login")
def login(email: str, password: str):
    db: Session = SessionLocal()
    u = db.exec(__import__("sqlmodel").select(User).where(User.email==email)).first()
    if not u or not pwd.verify(password, u.password_hash):
        return {"ok": False}
    return {"token": f"demo-token-{u.id}"}
