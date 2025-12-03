# backend/app/deps.py
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from backend.app.db import SessionLocal
from backend.app import settings
from backend.app.models import User
from backend.app.models_company import Company

auth_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_actor(token: Optional[Depends] = Depends(auth_scheme)) -> Dict[str, Any]:
    """
    Return an actor dict:
      {"type":"admin","user":User}
      {"type":"company","company":Company}
      {"type":"admin_company_access","admin_id":int,"company_id":int}
    Raises 401 on invalid token.
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid auth token")

    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise credentials_exception

    sub = payload.get("sub")
    typ = payload.get("type")
    db = SessionLocal()
    try:
        # Company token
        if typ == "company":
            try:
                cid = int(sub)
            except Exception:
                raise credentials_exception
            company = db.get(Company, cid)
            if not company:
                raise credentials_exception
            return {"type": "company", "company": company}

        # Temporary admin->company access token
        if typ == "admin_company_access":
            admin_id = payload.get("sub")
            company_id = payload.get("company_id")
            if not admin_id or not company_id:
                raise credentials_exception
            return {"type": "admin_company_access", "admin_id": int(admin_id), "company_id": int(company_id)}

        # Default: admin/user token
        # older tokens may not set type; try user lookup
        try:
            uid = int(sub)
        except Exception:
            raise credentials_exception

        user = db.get(User, uid)
        if not user:
            raise credentials_exception
        return {"type": "admin", "user": user}
    finally:
        db.close()
