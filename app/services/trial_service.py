from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from app.models_trial import TrialSettings
from app.models import Subscription, Company  # assumes existing models
from sqlmodel import SQLModel

def get_trial_settings(session: Session) -> Optional[TrialSettings]:
    stmt = select(TrialSettings).limit(1)
    result = session.exec(stmt).first()
    return result

def create_one_time_trial_for_company(session: Session, company: Company, admin_id: Optional[int] = None) -> Optional[Subscription]:
    # Check if company already had trial
    if getattr(company, 'has_trial_once', False):
        return None
    settings = get_trial_settings(session)
    if not settings or not settings.trial_enabled or settings.trial_days <= 0:
        return None
    now = datetime.utcnow()
    end = now + timedelta(days=settings.trial_days)
    # Create subscription record (assumes Subscription model exists with these fields)
    sub = Subscription(
        company_id=company.id,
        plan_type='trial',
        start_date=now,
        end_date=end,
        amount=0.0,
        status='active',
        created_by=admin_id or 0,
    )
    session.add(sub)
    # mark company flags
    company.has_trial_once = True
    company.trial_started_at = now
    company.trial_ended_at = end
    session.add(company)
    session.commit()
    session.refresh(sub)
    return sub
