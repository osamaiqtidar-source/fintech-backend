import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Note: place Noto fonts under app/fonts and register them here for Unicode/RTL support
# pdfmetrics.registerFont(TTFont('NotoSans', '/app/fonts/NotoSans-Regular.ttf'))

def invoices_to_pdf_stream(invoices, title="Invoices"):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 24
    c.setFont("Helvetica", 9)
    for inv in invoices:
        line = f"{inv.get('date')} | {inv.get('invoice_number')} | {inv.get('customer_name')} | {inv.get('currency')} {inv.get('total')}"
        c.drawString(40, y, line[:150])
        y -= 14
        if y < 60:
            c.showPage()
            y = height - 40
    c.save()
    buf.seek(0)
    return buf
