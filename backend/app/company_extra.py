from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

    name: str = Field(sa_column=Column(String, nullable=False))

    credentials: Dict | None = Field(
        default=None,
        sa_column=Column(JSON)
    )
