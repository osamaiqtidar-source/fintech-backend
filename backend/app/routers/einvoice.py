# backend/app/routers/einvoice.py
from fastapi import APIRouter, Depends, HTTPException
from backend.app.deps import get_current_actor
from backend.app.db import SessionLocal
from backend.app import models
from backend.app.audit import log_admin_action

router = APIRouter()

@router.post("/request/{invoice_id}")
def request_einvoice(invoice_id: int, actor = Depends(get_current_actor)):
    db = SessionLocal()
    try:
        # Determine company context
        if actor["type"] == "company":
            cid = actor["company"].id
            admin_id = None
        elif actor["type"] == "admin_company_access":
            cid = actor["company_id"]
            admin_id = actor.get("admin_id")
        else:
            raise HTTPException(status_code=403, detail="Admin must request company access")

        inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id, models.Invoice.company_id == cid).first()
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Existing e-invoice processing logic (call your existing functions)
        # Example: result = generate_and_send_einvoice(db, inv)  # keep your existing einvoice logic
        # For now, call your existing module function - ensure it's imported
        from backend.app.einvoice import generate_einvoice_for_invoice
        result = generate_einvoice_for_invoice(db, inv)

        if admin_id:
            log_admin_action(db, admin_id, "request_einvoice_admin", cid, {"invoice_id": invoice_id})

        return result
    finally:
        db.close()
