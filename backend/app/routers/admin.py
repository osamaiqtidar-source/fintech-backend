# backend/app/admin.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from backend.app.deps import get_current_actor
from backend.app.db import SessionLocal, pwd_context
from backend.app.models.user import User
from backend.app.deps import require_admin, require_super_admin  # must return current User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------- Schemas ----------
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_dynamic_password: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    role: constr(regex="^(super_admin|admin|staff|viewer)$")
    password: Optional[constr(min_length=6)] = None
    is_dynamic_password: Optional[bool] = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[constr(regex="^(super_admin|admin|staff|viewer)$")] = None
    password: Optional[constr(min_length=6)] = None
    is_dynamic_password: Optional[bool] = None


class ChangeUsernameSchema(BaseModel):
    new_email: EmailStr


# ---------- Helpers ----------
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def check_admin_permissions(actor: User, target_role: str):
    """
    Enforce Option A rules:
    - super_admin: can manage anyone
    - admin: can manage only staff/viewer (cannot manage admin or super_admin)
    """
    if actor.role == "super_admin":
        return  # allowed

    if actor.role == "admin":
        if target_role in ("staff", "viewer"):
            return
        raise HTTPException(status_code=403, detail="Admins can only manage staff and viewer users")

    raise HTTPException(status_code=403, detail="Insufficient permissions")


# ---------- Endpoints ----------
@router.get("/users", response_model=List[UserOut])
def list_users(current=Depends(require_admin), db: Session = Depends(get_db)):
    """
    List all users. Admins and Super Admins can call this.
    """
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, current=Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, current=Depends(require_admin), db: Session = Depends(get_db)):
    # Check permissions: who can create which role
    check_admin_permissions(current, payload.role)

    # If is_dynamic_password True, we won't store a password_hash
    if payload.is_dynamic_password:
        password_hash = None
    else:
        if not payload.password:
            raise HTTPException(status_code=400, detail="Password required for non-dynamic users")
        password_hash = hash_password(payload.password)

    new_user = User(
        email=payload.email,
        role=payload.role,
        is_dynamic_password=bool(payload.is_dynamic_password),
        password_hash=password_hash
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, current=Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Admin trying to update target role? Check permission for the target role (if role change requested)
    target_role = payload.role if payload.role is not None else user.role
    check_admin_permissions(current, target_role)

    # Prevent admins from changing super_admin/email/role in ways they shouldn't
    # If an admin tries to modify an admin or super_admin (other than super_admin itself), forbid it
    if current.role == "admin":
        if user.role in ("admin", "super_admin"):
            raise HTTPException(status_code=403, detail="Admins cannot modify admins or super_admins")

    # Apply updates
    if payload.email:
        # ensure unique
        existing = db.query(User).filter(User.email == payload.email, User.id != user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = payload.email

    if payload.role:
        user.role = payload.role

    if payload.is_dynamic_password is not None:
        user.is_dynamic_password = bool(payload.is_dynamic_password)
        if user.is_dynamic_password:
            user.password_hash = None  # remove stored hash if switching to dynamic

    if payload.password:
        # setting password for non-dynamic user
        user.password_hash = hash_password(payload.password)
        user.is_dynamic_password = False

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}")
def delete_user(user_id: int, current=Depends(require_admin), db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Admin cannot delete admins or super_admins
    if current.role == "admin" and user.role in ("admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Admins cannot delete admins or super_admins")

    # Prevent super_admin from deleting themselves accidentally via this endpoint
    if current.role == "super_admin" and current.id == user_id:
        # Allow, but it's dangerous. You may want to block deletion of the last super_admin.
        pass

    try:
        db.delete(user)
        db.commit()
        return {"ok": True, "message": "User deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/me/username")
def change_own_username(payload: ChangeUsernameSchema, current=Depends(require_admin), db: Session = Depends(get_db)):
    """
    Change current user's email/username.
    Super admin can change his username as requested.
    """
    # check collision
    existing = db.query(User).filter(User.email == payload.new_email, User.id != current.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already taken")

    # Apply change
    user = db.get(User, current.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = payload.new_email
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"ok": True, "new_email": user.email}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# GDPR endpoints
from fastapi import BackgroundTasks
@router.post('/company/{company_id}/request-data-export')
def request_company_data_export(company_id: int, actor=Depends(get_current_actor), background_tasks: BackgroundTasks = None):
    if actor['type'] != 'admin':
        raise HTTPException(status_code=403, detail='Only admin can request exports')
    # schedule export (simple sync for now)
    from app.export.report_generator import generate_sales
    # generate minimal snapshot
    sales = generate_sales(company_id)
    # store to /tmp and log
    path = f"/tmp/company_{company_id}_export.json"
    import json
    with open(path,'w') as f:
        json.dump({'sales': sales}, f)
    log_admin_action(None, actor['user'].id, 'request_company_data_export', company_id, {'path': path})
    return {'ok': True, 'path': path}
@router.delete('/company/{company_id}/delete-data')
def delete_company_data(company_id: int, actor=Depends(get_current_actor)):
    if actor['type'] != 'admin':
        raise HTTPException(status_code=403, detail='Only admin can delete data')
    db = SessionLocal()
    try:
        # caution: destructive!
        db.execute('DELETE FROM invoice WHERE company_id = %s', (company_id,))
        db.execute('DELETE FROM admincompanyaccess WHERE company_id = %s', (company_id,))
        db.execute('DELETE FROM einvoice_log WHERE company_id = %s', (company_id,))
        db.commit()
        log_admin_action(db, actor['user'].id, 'delete_company_data', company_id, None)
        return {'ok': True, 'deleted': True}
    finally:
        db.close()

# Backup endpoints
from app.services.backup_service import backup_database_to_s3
@router.post('/backup-now')
def backup_now(actor=Depends(get_current_actor)):
    if actor['type'] != 'admin':
        raise HTTPException(status_code=403, detail='Only admin can trigger backups')
    res = backup_database_to_s3(tag='manual')
    return {'ok': True, 'result': res}
