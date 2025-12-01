from fastapi import APIRouter, Body, Depends, HTTPException
from ..deps import require_connector
from ..db import get_session
from ..models import SyncOperation
from ..schemas import ConnectorUpload
from sqlmodel import select
from datetime import datetime

router = APIRouter(dependencies=[Depends(require_connector)])

@router.get('/{company_id}/connector/pending')
def connector_pending(company_id: int, limit: int = 50):
    session = get_session()
    q = select(SyncOperation).where(SyncOperation.company_id == company_id, SyncOperation.source == 'mobile', SyncOperation.status == 'pending').limit(limit)
    rows = session.exec(q).all()
    return {'operations': [r.dict() for r in rows]}

@router.post('/{company_id}/connector/ack')
def connector_ack(company_id: int, ack: list = Body(...)):
    session = get_session()
    results = []
    for a in ack:
        op_id = a.get('op_id') or a.get('id')
        if not op_id:
            continue
        op = session.get(SyncOperation, op_id)
        if not op:
            results.append({'op_id': op_id, 'status': 'unknown'})
            continue
        if a.get('success'):
            op.status = 'synced'
            op.processed_at = datetime.utcnow()
        else:
            op.status = 'failed'
            op.attempts = (op.attempts or 0) + 1
        session.add(op)
        results.append({'op_id': op_id, 'status': op.status})
    session.commit()
    return {'results': results}

@router.post('/{company_id}/connector/upload')
def connector_upload(company_id: int, upload: ConnectorUpload):
    session = get_session()
    count = 0
    for ch in upload.changes:
        q = select(SyncOperation).where(SyncOperation.idempotency_key == ch.change_id, SyncOperation.company_id == company_id)
        if session.exec(q).first():
            continue
        so = SyncOperation(company_id=company_id, source='connector', operation_type=ch.type, payload=ch.payload, idempotency_key=ch.change_id, status='pending', created_at=datetime.utcnow())
        session.add(so)
        count += 1
    session.commit()
    return {'ok': True, 'received': count}

@router.post('/{company_id}/connector/update')
def connector_update(company_id: int, data: dict = Body(...)):
    session = get_session()
    so = SyncOperation(company_id=company_id, source='connector', operation_type='connector_update', payload=data, idempotency_key=None, status='synced', created_at=datetime.utcnow())
    session.add(so)
    session.commit()
    return {'ok': True}
