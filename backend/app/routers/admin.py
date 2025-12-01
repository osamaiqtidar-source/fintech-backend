from fastapi import APIRouter, Body, Depends, HTTPException
from ..db import get_session
from ..models import Subscription, User
from ..schemas import UserCreate
from sqlmodel import select
from datetime import datetime
from ..deps import get_current_user

router = APIRouter()

@router.post('/subscriptions/start')
def start_subscription(data: dict = Body(...), admin = Depends(get_current_user)):
    # only admin allowed
    if not admin.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    session = get_session()
    start = datetime.utcnow()
    end = start.replace(year=start.year + (data.get('months', 12) // 12))
    sub = Subscription(company_id=data['company_id'], plan_type=data['plan_type'], start_date=start, end_date=end, price=data.get('price', 0), created_by_admin=True, notes=data.get('notes'))
    session.add(sub)
    users = session.exec(select(User).where(User.company_id == data['company_id'])).all()
    for u in users:
        u.subscription_plan = data['plan_type']
        session.add(u)
    session.commit()
    return {'ok': True, 'subscription_id': sub.id}

@router.get('/subscriptions/expiring')
def expiring(days: int = 7, admin = Depends(get_current_user)):
    if not admin.is_admin:
        raise HTTPException(status_code=403, detail='Admin only')
    session = get_session()
    rows = session.exec(select(Subscription).where(Subscription.status == 'active')).all()
    out = []
    now = datetime.utcnow()
    for r in rows:
        if r.end_date:
            delta = (r.end_date - now).days
            if delta <= days:
                out.append({'id': r.id, 'company_id': r.company_id, 'plan_type': r.plan_type, 'end_date': r.end_date.isoformat(), 'days_remaining': delta})
    return {'expiring': out}
