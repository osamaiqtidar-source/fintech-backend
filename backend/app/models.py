
from typing import Optional, Dict, Any, List
from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tally_identifier: Optional[str] = None
    country_code: Optional[str] = None
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
    payload: Optional[Dict[str,Any]] = Field(default=None, sa_column=Column(JSONB, nullable=True))
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

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int
    created_by_user_id: Optional[int] = None
    items: Optional[List[Dict[str,Any]]] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    totals: Optional[Dict[str,Any]] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    tax_details: Optional[Dict[str,Any]] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    status: str = Field(default='created')
    qr_raw: Optional[str] = None
    qr_base64: Optional[str] = None
    e_invoice_meta: Optional[Dict[str,Any]] = Field(default=None, sa_column=Column(JSONB, nullable=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)
