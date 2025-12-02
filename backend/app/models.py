from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, String, func

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # FIXED — no index=True with sa_column, type is mandatory
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))

    password_hash: str = Field(sa_column=Column(String, nullable=False))

    role: str = Field(default="staff", sa_column=Column(String, nullable=False))

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=func.now())
    )
