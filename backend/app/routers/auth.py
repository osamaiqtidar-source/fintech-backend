from fastapi import APIRouter,HTTPException
from sqlmodel import Session
from ..db import SessionLocal
from .. import models
from passlib.context import CryptContext
from jose import jwt
import time, os
router=APIRouter()
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto')
SECRET=os.getenv('SECRET_KEY','secret')
ALGO='HS256'
EXP=60*60*24*30
@router.post('/register')
def register(email:str,password:str):
    db=SessionLocal()
    h=pwd.hash(password)
    u=models.User(email=email,password_hash=h)
    db.add(u);db.commit();db.refresh(u)
    return {'ok':True,'user_id':u.id}
@router.post('/login')
def login(email:str,password:str):
    db=SessionLocal()
    u=db.exec(__import__('sqlmodel').select(models.User).where(models.User.email==email)).first()
    if not u or not pwd.verify(password,u.password_hash):
        raise HTTPException(400,'Invalid')
    token={'sub':str(u.id),'exp':int(time.time())+EXP}
    return {'access_token':jwt.encode(token,SECRET,algorithm=ALGO)}
