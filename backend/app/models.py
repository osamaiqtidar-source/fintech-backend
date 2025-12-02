from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, String, func

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Correct email column
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))

    password_hash: str = Field(sa_column=Column(String, nullable=False))

    # Correct RBAC field
    role: str = Field(default="staff", sa_column=Column(String, nullable=False))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )
