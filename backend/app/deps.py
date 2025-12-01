import os
from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token
from .db import get_session
from .models import User
from sqlmodel import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

def require_connector(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing connector key')
    key = authorization.replace('Api-Key ', '')
    if key != os.getenv('CONNECTOR_API_KEY'):
        raise HTTPException(status_code=401, detail='Invalid connector key')
    return True

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=401, detail='Invalid auth token')
    email = payload['sub']
    session = get_session()
    q = select(User).where(User.email == email)
    user = session.exec(q).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user
