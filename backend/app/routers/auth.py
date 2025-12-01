from fastapi import APIRouter, Depends, HTTPException
from ..schemas import LoginRequest, Token, UserCreate
from ..security import verify_password, get_password_hash, create_access_token
from ..db import get_session
from ..models import User
from sqlmodel import select

router = APIRouter()

@router.post('/token', response_model=Token)
def token(data: LoginRequest):
    session = get_session()
    q = select(User).where(User.email == data.email)
    user = session.exec(q).first()
    if not user or not verify_password(data.password, user.password_hash or ''):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = create_access_token({'sub': user.email})
    return {'access_token': access, 'token_type': 'bearer'}
