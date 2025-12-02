from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .db import SessionLocal
try:
    from .models import User
except Exception:
    User = None
try:
    from .settings import settings
except Exception:
    class settings:
        JWT_SECRET = "CHANGE_ME"
auth_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: dict = Depends(auth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if User is None:
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

def require_super_admin(user=Depends(get_current_user)):
    if getattr(user, "role", None) != "super_admin":
        raise HTTPException(status_code=403, detail="Super Admin only")
    return user

def require_admin(user=Depends(get_current_user)):
    if getattr(user, "role", None) not in ("super_admin", "admin"):
        raise HTTPException(status_code=403, detail="Admins only")
    return user

def require_staff(user=Depends(get_current_user)):
    if getattr(user, "role", None) not in ("super_admin", "admin", "staff"):
        raise HTTPException(status_code=403, detail="Staff or above only")
    return user

def require_viewer(user=Depends(get_current_user)):
    if getattr(user, "role", None) not in ("super_admin", "admin", "staff", "viewer"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user
