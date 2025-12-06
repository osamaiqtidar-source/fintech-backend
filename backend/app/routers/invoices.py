from fastapi import APIRouter,HTTPException
from ..db import SessionLocal
from .. import models
from ..services.tax_engine import validate_and_calculate_tax
router=APIRouter()
@router.post('/create')
def create_invoice(payload:dict):
    db=SessionLocal()
    inv=models.Invoice(company_id=payload['company_id'],items=payload.get('items'),totals=payload.get('totals'),tax_details=payload.get('tax_details'),e_invoice_meta=payload.get('e_invoice_meta'))
    db.add(inv);db.commit();db.refresh(inv)
    res=validate_and_calculate_tax(db,inv)
    if not res.get('ok'):
        db.delete(inv);db.commit()
        raise HTTPException(status_code=400,detail=res.get('error'))
    inv=res.get('invoice')
    db.add(inv);db.commit();db.refresh(inv)
    return {'ok':True,'invoice_id':inv.id}
