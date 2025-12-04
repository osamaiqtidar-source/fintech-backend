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

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )
