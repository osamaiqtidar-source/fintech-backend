
from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlmodel import Session, select
from ..db import SessionLocal
from .. import models_extra, models
from ..tasks import submit_einvoice_worker

router = APIRouter()

@router.post("/request/{invoice_id}")
def request_einvoice(invoice_id: int, background_tasks: BackgroundTasks):
    db: Session = SessionLocal()
    inv = db.get(models.Invoice, invoice_id)
    if not inv:
        raise HTTPException(404, "Invoice not found")
    country = (inv.e_invoice_meta or {}).get("country") or "IN"
    q = select(models_extra.EInvoiceProvider).where(models_extra.EInvoiceProvider.country==country, models_extra.EInvoiceProvider.enabled==True).order_by(models_extra.EInvoiceProvider.priority)
    provider = db.exec(q).first()
    if not provider:
        raise HTTPException(503, "No provider configured")
    payload = {"invoice_id": inv.id, "company_id": inv.company_id, "items": inv.items, "totals": inv.totals, "tax": inv.tax_details, "country": country}
    sub = models_extra.EInvoiceSubmission(invoice_id=inv.id, company_id=inv.company_id, provider_id=provider.id, provider_name=provider.provider_name, country=country, request_payload=payload)
    db.add(sub); db.commit(); db.refresh(sub)
    background_tasks.add_task(submit_einvoice_worker, sub.id)
    return {"ok": True, "submission_id": sub.id}
