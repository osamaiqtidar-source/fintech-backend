# ----------------------------------------------------
#   MODELS EXTRA - CLEANED & FIXED
# ----------------------------------------------------

from sqlmodel import SQLModel, Field
from typing import Optional, Any
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Boolean,
    Integer,
    JSON,
)


# ----------------------------------------------------
#   USER MODEL
# ----------------------------------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(sa_column=Column(String, unique=True, nullable=False))

    password_hash: Optional[str] = Field(
        default=None,
        sa_column=Column(String, nullable=True)
    )

    role: str = Field(default="staff", sa_column=Column(String, nullable=False))

    is_dynamic_password: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False, server_default="false")
    )

    created_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )


# ----------------------------------------------------
#   COMPANY MODEL
# ----------------------------------------------------
class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(sa_column=Column(String, nullable=False))

    email: Optional[str] = Field(default=None, sa_column=Column(String, unique=True))
    phone: str = Field(sa_column=Column(String, unique=True, nullable=False))

    otp_code: Optional[str] = Field(default=None, sa_column=Column(String))

    otp_expires_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime)
    )

    subscription_plan: str = Field(
        default="free",
        sa_column=Column(String, nullable=False, server_default="free")
    )

    created_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )


# ----------------------------------------------------
#   ADMIN ACCESS MODEL
# ----------------------------------------------------
class AdminCompanyAccess(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    admin_id: int = Field(sa_column=Column(Integer, nullable=False))
    company_id: int = Field(sa_column=Column(Integer, nullable=False))

    otp: Optional[str] = Field(default=None, sa_column=Column(String))

    # FIX: DateTime must map to datetime | None
    expires_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=False))
    )

    approved: bool = Field(default=False, sa_column=Column(Boolean, server_default="false"))

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=False), server_default=func.now())
    )


# ----------------------------------------------------
#   E-INVOICE PROVIDER
# ----------------------------------------------------
class EInvoiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(sa_column=Column(String, nullable=False))
    country: str = Field(sa_column=Column(String, nullable=False))

    priority: int = Field(default=100, sa_column=Column(Integer, nullable=False))

    config: Optional[Any] = Field(default=None, sa_column=Column(JSON))

    encrypted_credentials_ref: Optional[str] = Field(default=None, sa_column=Column(String))

    enabled: bool = Field(default=True, sa_column=Column(Boolean, server_default='true'))

    # FIX: correct type
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now())
    )


# ----------------------------------------------------
#   E-INVOICE LOG
# ----------------------------------------------------
class EInvoiceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    invoice_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    provider_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    company_id: Optional[int] = Field(default=None, sa_column=Column(Integer))

    request_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    response_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))

    status: Optional[str] = Field(default=None, sa_column=Column(String))

    # FIX: correct datetime type
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime, server_default=func.now())
    )
