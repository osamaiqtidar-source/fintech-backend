from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

class CompanyExtra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # FIXED: Explicit String type required
    name: str = Field(sa_column=Column(String, nullable=False))

    # FIXED: JSON type is supported
    credentials: Dict | None = Field(default=None, sa_column=Column(JSON))
