
from .db import SessionLocal
from . import models_extra, models
import time

def submit_einvoice_worker(submission_id: int):
    db = SessionLocal()
    sub = db.get(models_extra.EInvoiceSubmission, submission_id)
    if not sub:
        return
    # Mock submission: produce a fake IRN and mark submitted
    time.sleep(1)
    sub.response_payload = {"irn": f"IRN-{submission_id}"}
    sub.irn_or_uuid = sub.response_payload["irn"]
    sub.status = "submitted"
    db.add(sub); db.commit()
    inv = db.get(models.Invoice, sub.invoice_id)
    inv.e_invoice_meta = inv.e_invoice_meta or {}
    inv.e_invoice_meta["irn"] = sub.irn_or_uuid
    db.add(inv); db.commit()
