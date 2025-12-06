import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.utils.translator import translate
# Optional RTL support
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _RTL_AVAILABLE = True
except Exception:
    _RTL_AVAILABLE = False

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# Note: place Noto fonts under app/fonts and register them here for Unicode/RTL support
# pdfmetrics.registerFont(TTFont('NotoSans', '/app/fonts/NotoSans-Regular.ttf'))

def invoices_to_pdf_stream(invoices, title="Invoices", company_language='en'):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    title_text = translate('invoice_title', company_language) if title == 'Invoices' else title
    if _RTL_AVAILABLE and company_language in ('ar', 'he'):
        try:
            title_text = get_display(arabic_reshaper.reshape(title_text))
        except Exception:
            pass
    c.drawString(40, y, title_text)
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
