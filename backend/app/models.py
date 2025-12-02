from typing import Optional,Dict,Any,List
from sqlmodel import SQLModel,Field,Column
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
class Company(SQLModel, table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    name:str
    tally_identifier:Optional[str]=None
    country_code:Optional[str]=None
    created_at:datetime=Field(default_factory=datetime.utcnow)
class User(SQLModel, table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    company_id:Optional[int]=None
    email:str
    mobile:Optional[str]=None
    password_hash:Optional[str]=None
    roles:Optional[str]=None
    subscription_plan:str=Field(default='basic')
    is_admin:bool=Field(default=False)
    created_at:datetime=Field(default_factory=datetime.utcnow)
