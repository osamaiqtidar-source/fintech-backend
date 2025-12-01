from fastapi import APIRouter, Body, HTTPException, Depends
from ..schemas import UserCreate
from ..db import get_session
from ..models import User
from ..security import get_password_hash
from sqlmodel import select

router = APIRouter()

@router.post('/create')
def create_user(data: UserCreate = Body(...)):
    session = get_session()
    q = select(User).where(User.email == data.email)
    if session.exec(q).first():
        raise HTTPException(status_code=400, detail='Email exists')
    user = User(company_id=data.company_id, email=data.email, password_hash=get_password_hash(data.password), is_admin=data.is_admin, subscription_plan='basic')
    session.add(user)
    session.commit()
    session.refresh(user)
    return {'id': user.id, 'email': user.email}
