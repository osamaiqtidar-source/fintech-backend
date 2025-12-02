from fastapi import APIRouter,Header,HTTPException
from ..db import SessionLocal
from .. import models
import os
router=APIRouter()
CONNECTOR_API_KEY=os.getenv('CONNECTOR_API_KEY','connector-secret')
@router.post('/register')
def register(connector_name:str,x_connector_key:str=Header(None)):
    if x_connector_key!=CONNECTOR_API_KEY:
        raise HTTPException(403,'Invalid connector key')
    return {'ok':True,'registered':connector_name}
@router.post('/sync')
def sync(op:dict,x_connector_key:str=Header(None)):
    if x_connector_key!=CONNECTOR_API_KEY:
        raise HTTPException(403,'Invalid connector key')
    db=SessionLocal()
    sop=models.SyncOperation(company_id=op.get('company_id',0),source=op.get('source','connector'),operation_type=op.get('type','sync'),payload=op.get('payload'))
    db.add(sop);db.commit();db.refresh(sop)
    return {'ok':True,'sync_id':sop.id}