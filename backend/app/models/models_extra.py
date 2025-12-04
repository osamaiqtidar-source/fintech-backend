# package


from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, String, func, Boolean

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Unique email
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))

    # Password hash is now OPTIONAL (super admin uses dynamic password)
    password_hash: Optional[str] = Field(
        default=None,
        sa_column=Column(String, nullable=True)
    )

    # RBAC role
    role: str = Field(default="staff", sa_column=Column(String, nullable=False))

    # NEW: dynamic password flag
    is_dynamic_password: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False, server_default="false")
    )

    created_at: datetime | None  = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )


from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String, DateTime, func
from typing import Optional
from datetime import datetime

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

    created_at: datetime | None  = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )


# backend/app/models_admin_access.py
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, String, DateTime, Boolean, func

class AdminCompanyAccess(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admin_id: int = Field(sa_column=Column(Integer, nullable=False))
    company_id: int = Field(sa_column=Column(Integer, nullable=False))
    otp: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    expires_at: Optional[str] = Field(default=None, sa_column=Column(DateTime(timezone=False)))
    approved: bool = Field(default=False, sa_column=Column(Boolean, server_default="false"))
    created_at: Optional[str] = Field(default=None, sa_column=Column(DateTime(timezone=False), server_default=func.now()))


from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

class EInvoiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, nullable=False))
    country: str = Field(sa_column=Column(String, nullable=False))
    priority: int = Field(default=100, sa_column=Column(Integer, nullable=False))
    config: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    encrypted_credentials_ref: Optional[str] = Field(default=None, sa_column=Column(String))
    enabled: bool = Field(default=True, sa_column=Column(Boolean, server_default='true'))
    created_at: Optional[DateTime] = Field(default=None, sa_column=Column(DateTime, server_default=func.now()))
class EInvoiceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    provider_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    company_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    request_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    response_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    status: Optional[str] = Field(default=None, sa_column=Column(String))
    created_at: Optional[DateTime] = Field(default=None, sa_column=Column(DateTime, server_default=func.now()))