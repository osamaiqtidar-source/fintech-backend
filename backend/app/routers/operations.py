from fastapi import APIRouter, Body, Depends, HTTPException
from ..schemas import OperationCreate
from ..db import get_session
from ..models import SyncOperation
from sqlmodel import select
from datetime import datetime
from ..deps import get_current_user

router = APIRouter()

@router.post('/{company_id}/operations')
def create_operation(company_id: int, op: OperationCreate = Body(...), user=Depends(get_current_user)):
    # enforce company match and subscription
    if user.company_id != company_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    if user.subscription_plan != 'full':
        raise HTTPException(status_code=403, detail='Full subscription required')
    session = get_session()
    if op.idempotency_key:
        q = select(SyncOperation).where(SyncOperation.idempotency_key == op.idempotency_key, SyncOperation.company_id == company_id)
        existing = session.exec(q).first()
        if existing:
            return {'id': existing.id, 'status': existing.status}
    so = SyncOperation(company_id=company_id, source='mobile', operation_type=op.operation_type, payload=op.payload, idempotency_key=op.idempotency_key, status='pending', created_at=datetime.utcnow())
    session.add(so)
    session.commit()
    session.refresh(so)
    return {'id': so.id, 'status': so.status}
