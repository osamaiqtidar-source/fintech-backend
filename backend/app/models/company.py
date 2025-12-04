# backend/app/models_admin_access.py
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, String, DateTime, Boolean, func

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime, func
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(sa_column=Column(String, nullable=False))

    # Single owner login contact
    email: Optional[str] = Field(default=None, sa_column=Column(String, unique=True))
    phone: str = Field(sa_column=Column(String, unique=True, nullable=False))

    # OTP-based login fields
    otp_code: Optional[str] = Field(default=None, sa_column=Column(String))
    otp_expires_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))

    # Consumer subscription plan
    subscription_plan: str = Field(
        default="free",
        sa_column=Column(String, nullable=False, server_default="free")
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )

class AdminCompanyAccess(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(sa_column=Column(Integer, nullable=False))
    company_id: int = Field(sa_column=Column(Integer, nullable=False))
    otp: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    expires_at: Optional[str] = Field(default=None, sa_column=Column(DateTime(timezone=False)))
    approved: bool = Field(default=False, sa_column=Column(Boolean, server_default="false"))
    created_at: Optional[str] = Field(default=None, sa_column=Column(DateTime(timezone=False), server_default=func.now()))

class CompanyExtra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Explicit type is required to avoid NullType
    name: str = Field(sa_column=Column(String, nullable=False))

    # JSON type is OK
    credentials: Dict | None = Field(default=None, sa_column=Column(JSON))
