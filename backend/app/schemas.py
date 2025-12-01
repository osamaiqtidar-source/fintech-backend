from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List

class UserCreate(BaseModel):
    company_id: int
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class LoginRequest(BaseModel):
    email: str
    password: str

class OperationCreate(BaseModel):
    idempotency_key: Optional[str]
    operation_type: str
    payload: Any

class ConnectorUploadItem(BaseModel):
    change_id: str
    type: str
    entity: str
    payload: Any
    timestamp: str

class ConnectorUpload(BaseModel):
    cursor: Optional[str]
    changes: List[ConnectorUploadItem]

class AppUpdateCreate(BaseModel):
    version: Optional[str]
    notes: Optional[str]
    payload: Optional[Any]
