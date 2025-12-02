from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON, Boolean
from typing import Optional

class TrialSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trial_enabled: bool = Field(default=True, nullable=False)
    trial_days: int = Field(default=14, nullable=False)
    feature_flags: Optional[dict] = Field(default=None, sa_column=Column(JSON), nullable=True)
    updated_by: Optional[int] = Field(default=None, nullable=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Extend companies table via mixin-like addition - if companies model exists, these fields
# should be merged into the companies model by developer. For safety we create a helper.
class CompanyTrialFields(SQLModel):
    has_trial_once: bool = Field(default=False, nullable=False)
    trial_started_at: Optional[datetime] = Field(default=None, nullable=True)
    trial_ended_at: Optional[datetime] = Field(default=None, nullable=True)
