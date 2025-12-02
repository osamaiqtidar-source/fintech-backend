from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON

class CompanyExtra(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column('name', nullable=False))
    credentials: Dict | None = Field(default=None, sa_column=Column(JSON))
