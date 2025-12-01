from fastapi import APIRouter
from ..db import get_session
from ..models import SyncOperation
from sqlmodel import select

router = APIRouter()

@router.get('/{company_id}/sync/changes')
def get_changes(company_id: int, limit: int = 100):
    session = get_session()
    q = select(SyncOperation).where(SyncOperation.company_id == company_id).order_by(SyncOperation.created_at.desc()).limit(limit)
    rows = session.exec(q).all()
    return {'changes': [r.dict() for r in rows]}
