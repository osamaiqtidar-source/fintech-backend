from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tally_identifier: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: Optional[int] = None
    email: str
    password_hash: Optional[str] = None
    roles: Optional[str] = None
    subscription_plan: str = Field(default='basic')
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SyncOperation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(index=True)
    source: str
    operation_type: str
    payload: dict = Field(sa_column=Column(nullable=False))
    idempotency_key: Optional[str] = Field(index=True, default=None)
    status: str = Field(default='pending')
    attempts: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int
    plan_type: str
    status: str = Field(default='active')
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    price: Optional[float] = None
    created_by_admin: bool = Field(default=False)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SubscriptionReminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subscription_id: int
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    method: str
    status: str
    message: Optional[str] = None

class AppUpdate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int
    version: Optional[str] = None
    notes: Optional[str] = None
    payload: Optional[dict] = Field(default=None, sa_column=Column(nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)
