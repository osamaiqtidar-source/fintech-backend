# backend/app/routers/invoices.py
from fastapi import APIRouter, Depends, HTTPException
from backend.app.deps import get_current_actor
from backend.app.db import SessionLocal
from backend.app import models
from backend.app.services.tax_engine import validate_and_calculate_tax
from backend.app.audit import log_admin_action

router = APIRouter()

@router.post("/create")
def create_invoice(payload: dict, actor = Depends(get_current_actor)):
    db = SessionLocal()
    try:
        # determine company_id
        if actor["type"] == "company":
            company_id = actor["company"].id
            admin_id = None
        elif actor["type"] == "admin_company_access":
            company_id = actor["company_id"]
            admin_id = actor["admin_id"] if "admin_id" in actor else actor.get("admin_id")
            # note: our get_current_actor returns admin_id only on token decode; ensure admin_id exists
        else:
            raise HTTPException(status_code=403, detail="Admin must request company access")

        inv = models.Invoice(
            company_id = company_id,
            invoice_number = payload.get("invoice_number"),
            date = payload.get("date"),
            customer_name = payload.get("customer_name"),
            items = payload.get("items"),
            taxable_value = payload.get("taxable_value"),
            tax_amount = payload.get("tax_amount"),
            total = payload.get("total"),
            tax_details = payload.get("tax_details"),
            e_invoice_meta = payload.get("e_invoice_meta")
        )

        # Validate tax BEFORE persist
        res = validate_and_calculate_tax(db, inv)
        if not res.get("ok"):
            raise HTTPException(status_code=400, detail=res.get("error"))

        db.add(inv); db.commit(); db.refresh(inv)

        if admin_id:
            log_admin_action(db, admin_id, "create_invoice_admin", company_id, {"invoice_id": inv.id})

        return {"ok": True, "invoice_id": inv.id}
    finally:
        db.close()

@router.get("/list")
def list_invoices(actor = Depends(get_current_actor)):
    db = SessionLocal()
    try:
        if actor["type"] == "company":
            cid = actor["company"].id
            admin_id = None
        elif actor["type"] == "admin_company_access":
            cid = actor["company_id"]
            admin_id = actor.get("admin_id")
        else:
            raise HTTPException(status_code=403, detail="Admin must request company access")

        rows = db.query(models.Invoice).filter(models.Invoice.company_id == cid).all()

        if admin_id:
            log_admin_action(db, admin_id, "list_invoices_admin", cid, {"count": len(rows)})

        return {"ok": True, "invoices": rows}
    finally:
        db.close()
