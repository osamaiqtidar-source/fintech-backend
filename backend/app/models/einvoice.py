from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, func

class EInvoiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, nullable=False))
    country: str = Field(sa_column=Column(String, nullable=False))
    priority: int = Field(default=100, sa_column=Column(Integer, nullable=False))
    config: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    encrypted_credentials_ref: Optional[str] = Field(default=None, sa_column=Column(String))
    enabled: bool = Field(default=True, sa_column=Column(Boolean, server_default='true'))
    created_at: Optional[DateTime] = Field(default=None, sa_column=Column(DateTime, server_default=func.now()))

class EInvoiceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    provider_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    company_id: Optional[int] = Field(default=None, sa_column=Column(Integer))
    request_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    response_payload: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    status: Optional[str] = Field(default=None, sa_column=Column(String))
    created_at: Optional[DateTime] = Field(default=None, sa_column=Column(DateTime, server_default=func.now()))
