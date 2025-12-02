from sqlmodel import SQLModel,Field
from typing import Optional,Dict,Any
from datetime import datetime
class EInvoiceProvider(SQLModel, table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    country:str
    provider_name:str
    type:str=Field(default='B')
    enabled:bool=Field(default=False)
    priority:int=Field(default=100)
    credentials:Optional[Dict[str,Any]]=Field(default=None)
    endpoint_url:Optional[str]=None
    webhook_secret:Optional[str]=None
    cert_blob_id:Optional[str]=None
    notes:Optional[str]=None
    created_at:datetime=Field(default_factory=datetime.utcnow)
