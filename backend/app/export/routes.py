from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from backend.app.deps import get_current_actor
from .report_generator import generate_sales, generate_purchase, generate_gst_summary
from .csv_export import invoices_to_csv_string
from .excel_export import invoices_to_xlsx_stream
from .pdf_export import invoices_to_pdf_stream
from .tally_xml_export import invoices_to_tally_xml_string
from .zip_export import create_zip_stream
export_router = APIRouter()
def _company_id(actor, company_id_param):
    if actor["type"] == "company":
        return actor["company"].id
    if actor["type"] == "admin_company_access":
        return actor["company_id"]
    if actor["type"] == "admin":
        if company_id_param:
            return int(company_id_param)
        raise HTTPException(status_code=400, detail="company_id required for admin")
    raise HTTPException(status_code=401, detail="Invalid actor")
@export_router.get("/sales")
def export_sales(format: str = Query("csv"), company_id: int | None = None, start: str | None = None, end: str | None = None, actor = Depends(get_current_actor)):
    cid = _company_id(actor, company_id)
    sales = generate_sales(cid, start, end)
    if format == "csv":
        csv_str = invoices_to_csv_string(sales)
        return StreamingResponse(iter([csv_str]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=sales.csv"})
    if format == "xlsx":
        xls = invoices_to_xlsx_stream(sales)
        return StreamingResponse(xls, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition":"attachment; filename=sales.xlsx"})
    if format == "pdf":
        pdf = invoices_to_pdf_stream(sales, title="Sales Report")
        return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition":"attachment; filename=sales.pdf"})
    if format == "tally":
        xml = invoices_to_tally_xml_string(sales)
        return StreamingResponse(iter([xml]), media_type="application/xml", headers={"Content-Disposition":"attachment; filename=sales_tally.xml"})
    if format == "zip":
        files = {
            "sales.csv": invoices_to_csv_string(sales),
            "sales.xlsx": invoices_to_xlsx_stream(sales).getvalue(),
            "sales.pdf": invoices_to_pdf_stream(sales, title="Sales Report").getvalue(),
            "sales_tally.xml": invoices_to_tally_xml_string(sales)
        }
        z = create_zip_stream(files)
        return StreamingResponse(z, media_type="application/zip", headers={"Content-Disposition":"attachment; filename=sales_export.zip"})
    raise HTTPException(status_code=400, detail="invalid format")
@export_router.get("/purchase")
def export_purchase(format: str = Query("csv"), company_id: int | None = None, start: str | None = None, end: str | None = None, actor = Depends(get_current_actor)):
    cid = _company_id(actor, company_id)
    purchases = generate_purchase(cid, start, end)
    if format == "csv":
        return StreamingResponse(iter([invoices_to_csv_string(purchases)]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=purchase.csv"})
    if format == "xlsx":
        return StreamingResponse(invoices_to_xlsx_stream(purchases), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition":"attachment; filename=purchase.xlsx"})
    if format == "pdf":
        return StreamingResponse(invoices_to_pdf_stream(purchases, title="Purchase Report"), media_type="application/pdf", headers={"Content-Disposition":"attachment; filename=purchase.pdf"})
    if format == "zip":
        files = {
            "purchase.csv": invoices_to_csv_string(purchases),
            "purchase.xlsx": invoices_to_xlsx_stream(purchases).getvalue(),
            "purchase.pdf": invoices_to_pdf_stream(purchases, title="Purchase Report").getvalue()
        }
        return StreamingResponse(create_zip_stream(files), media_type="application/zip", headers={"Content-Disposition":"attachment; filename=purchase_export.zip"})
    raise HTTPException(status_code=400, detail="invalid format")
@export_router.get("/gst")
def export_gst(format: str = Query("csv"), company_id: int | None = None, start: str | None = None, end: str | None = None, actor = Depends(get_current_actor)):
    cid = _company_id(actor, company_id)
    gst = generate_gst_summary(cid, start, end)
    if format == "json":
        return gst
    if format == "csv":
        csv_str = f"taxable_sum,tax_sum\n{gst['taxable_sum']},{gst['tax_sum']}\n"
        return StreamingResponse(iter([csv_str]), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=gst_summary.csv"})
    raise HTTPException(status_code=400, detail="invalid format")
