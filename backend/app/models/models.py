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
