from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

class CompanyExtra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Explicit type is required to avoid NullType
    name: str = Field(sa_column=Column(String, nullable=False))

    # JSON type is OK
    credentials: Dict | None = Field(default=None, sa_column=Column(JSON))
