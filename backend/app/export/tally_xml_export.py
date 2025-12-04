from xml.sax.saxutils import escape
def invoices_to_tally_xml_string(invoices, company_name="Company"):
    def fmt(dt):
        if dt is None:
            return ""
        if isinstance(dt, str):
            return dt.replace("-", "")
        return dt.strftime("%Y%m%d")
    parts = ['<ENVELOPE><HEADER><TALLYREQUEST>Import Data</TALLYREQUEST></HEADER><BODY><IMPORTDATA><REQUESTDESC><REPORTNAME>Vouchers</REPORTNAME></REQUESTDESC><REQUESTDATA>']
    for inv in invoices:
        parts.append(f"""\n<TALLYMESSAGE>\n<VOUCHER ACTION=\"Create\" VCHTYPE=\"{escape(inv.get('type','Sales'))}\">\n<DATE>{fmt(inv.get('date'))}</DATE>\n<PARTYNAME>{escape(str(inv.get('customer_name') or ''))}</PARTYNAME>\n<VOUCHERNUMBER>{escape(str(inv.get('invoice_number') or ''))}</VOUCHERNUMBER>\n<AMOUNT>{inv.get('total') or 0}</AMOUNT>\n</VOUCHER>\n</TALLYMESSAGE>""")
    parts.append('\n</REQUESTDATA></IMPORTDATA></BODY></ENVELOPE>')
    return "".join(parts)
