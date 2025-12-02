from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import Optional
from pydantic import BaseModel
from app.db import get_session
from app.models_trial import TrialSettings
from datetime import datetime

router = APIRouter(prefix='/admin/subscription', tags=['admin','subscription'])

class TrialSettingsIn(BaseModel):
    trial_enabled: bool
    trial_days: int
    feature_flags: Optional[dict] = None

@router.get('/trial-settings')
def get_trial_settings(session: Session = Depends(get_session)):
    stmt = select(TrialSettings).limit(1)
    settings = session.exec(stmt).first()
    if not settings:
        # return defaults
        return { 'trial_enabled': False, 'trial_days': 0, 'feature_flags': {} }
    return settings

@router.post('/trial-settings')
def create_or_update_trial_settings(payload: TrialSettingsIn, session: Session = Depends(get_session)):
    stmt = select(TrialSettings).limit(1)
    settings = session.exec(stmt).first()
    now = datetime.utcnow()
    if not settings:
        settings = TrialSettings(
            trial_enabled=payload.trial_enabled,
            trial_days=payload.trial_days,
            feature_flags=payload.feature_flags,
            updated_at=now,
            updated_by=None
        )
        session.add(settings)
    else:
        settings.trial_enabled = payload.trial_enabled
        settings.trial_days = payload.trial_days
        settings.feature_flags = payload.feature_flags
        settings.updated_at = now
    session.commit()
    session.refresh(settings)
    return settings
