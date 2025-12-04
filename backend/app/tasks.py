from .db import SessionLocal
from . import models_extra, models
import time

def submit_einvoice_worker(submission_id:int):
    db=SessionLocal()
    sub=db.get(models_extra.EInvoiceSubmission,submission_id)
    if not sub:
        return
    time.sleep(1)
    resp={'irn':f'IRN-{submission_id}','qr_raw':'TLV-EXAMPLE'}
    sub.response_payload=resp
    sub.irn_or_uuid=resp.get('irn')
    sub.qr_raw=resp.get('qr_raw')
    sub.status='submitted'
    db.add(sub);db.commit()
    inv=db.get(models.Invoice,sub.invoice_id)
    inv.e_invoice_meta=inv.e_invoice_meta or {}
    inv.e_invoice_meta['irn']=sub.irn_or_uuid
    inv.qr_raw=sub.qr_raw
    db.add(inv);db.commit()
