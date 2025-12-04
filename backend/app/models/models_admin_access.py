from datetime import datetime
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
