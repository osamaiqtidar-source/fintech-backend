
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class EInvoiceProvider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    country: str
    provider_name: str
    type: str = Field(default='B')
    enabled: bool = Field(default=False)
    priority: int = Field(default=100)
    credentials: Optional[dict] = Field(default=None)
    endpoint_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    cert_blob_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EInvoiceSubmission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int
    company_id: int
    provider_id: Optional[int] = None
    provider_name: Optional[str] = None
    country: str
    request_payload: Optional[dict] = Field(default=None)
    response_payload: Optional[dict] = Field(default=None)
    status: str = Field(default='pending')
    attempts: int = Field(default=0)
    last_error: Optional[str] = None
    irn_or_uuid: Optional[str] = None
    qr_raw: Optional[str] = None
    qr_base64: Optional[str] = None
    signed_invoice: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CompanyZatcaConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int
    status: str = Field(default="not_onboarded")
    private_key_blob_id: Optional[str] = None
    csr_blob_id: Optional[str] = None
    certificate_blob_id: Optional[str] = None
    csid: Optional[str] = None
    onboarded_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
