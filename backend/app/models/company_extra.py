from sqlmodel import SQLModel, Field
from typing import Optional, Dict
from sqlalchemy import Column, JSON, String

class CompanyExtra(SQLModel, table=True):
    """Extra metadata associated with a company.
    Stores credentials, integration parameters, or structured JSON config.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(sa_column=Column(String, nullable=False))

    credentials: Dict | None = Field(
        default=None,
        sa_column=Column(JSON)
    )
