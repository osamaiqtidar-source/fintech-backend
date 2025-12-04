import csv, io
def invoices_to_csv_string(invoices):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["id","invoice_number","date","type","customer_name","currency","taxable_value","tax_amount","total","items"])
    for inv in invoices:
        w.writerow([
            inv.get("id"),
            inv.get("invoice_number"),
            str(inv.get("date") or ""),
            inv.get("type"),
            inv.get("customer_name"),
            inv.get("currency"),
            inv.get("taxable_value"),
            inv.get("tax_amount"),
            inv.get("total"),
            inv.get("items"),
        ])
    return out.getvalue()
