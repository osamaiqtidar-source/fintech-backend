from backend.app.db import SessionLocal
from sqlalchemy import text
def _row_to_dict(r):
    try:
        return dict(r)
    except Exception:
        d = {}
        for k in r.__dict__.keys():
            if k.startswith("_"):
                continue
            d[k] = getattr(r, k)
        return d
def fetch_invoices(company_id, start=None, end=None, inv_type=None):
    db = SessionLocal()
    try:
        q = "SELECT id, company_id, invoice_number, date, type, customer_name, items, taxable_value, tax_amount, total, currency FROM invoice WHERE company_id = :cid"
        params = {"cid": company_id}
        if start:
            q += " AND date >= :start"; params["start"] = start
        if end:
            q += " AND date <= :end"; params["end"] = end
        if inv_type:
            q += " AND type = :itype"; params["itype"] = inv_type
        rows = db.execute(text(q), params).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        db.close()
def generate_sales(company_id, start=None, end=None):
    return fetch_invoices(company_id, start, end, inv_type="sale")
def generate_purchase(company_id, start=None, end=None):
    return fetch_invoices(company_id, start, end, inv_type="purchase")
def generate_gst_summary(company_id, start=None, end=None):
    db = SessionLocal()
    try:
        q = "SELECT COALESCE(SUM(taxable_value),0) as taxable_sum, COALESCE(SUM(tax_amount),0) as tax_sum FROM invoice WHERE company_id = :cid"
        params = {"cid": company_id}
        if start:
            q += " AND date >= :start"; params["start"] = start
        if end:
            q += " AND date <= :end"; params["end"] = end
        res = db.execute(text(q), params).fetchone()
        return {"taxable_sum": float(res[0] or 0), "tax_sum": float(res[1] or 0)}
    finally:
        db.close()
