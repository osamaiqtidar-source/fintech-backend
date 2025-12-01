from fastapi import APIRouter, Body, Depends
from ..db import get_session
from ..models import AppUpdate
from ..schemas import AppUpdateCreate
from datetime import datetime
from sqlmodel import select
from ..deps import get_current_user

router = APIRouter()

@router.post('/{company_id}/app/updates')
def create_update(company_id: int, upd: AppUpdateCreate = Body(...), admin = Depends(get_current_user)):
    if not admin.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    session = get_session()
    au = AppUpdate(company_id=company_id, version=upd.version, notes=upd.notes, payload=upd.payload, created_at=datetime.utcnow())
    session.add(au)
    session.commit()
    return {'ok': True, 'update_id': au.id}

@router.get('/{company_id}/app/updates')
def list_updates(company_id: int, limit: int = 20):
    session = get_session()
    rows = session.exec(select(AppUpdate).where(AppUpdate.company_id == company_id).order_by(AppUpdate.created_at.desc()).limit(limit)).all()
    return {'updates': [r.dict() for r in rows]}
