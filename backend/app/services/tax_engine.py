from sqlmodel import select
from backend.app import models

def validate_and_calculate_tax(db,invoice):
    country=(invoice.e_invoice_meta or {}).get('country')
    if not country:
        return {'ok':True,'invoice':invoice}
    q=select(models.TaxConfig).where(models.TaxConfig.country==country)
    cfg=db.exec(q).first()
    if not cfg:
        return {'ok':True,'invoice':invoice}
    config=cfg.config or {}
    if config.get('type')=='VAT':
        rate=config.get('rate',0)
        subtotal=(invoice.totals or {}).get('subtotal',0)
        expected=round(subtotal*rate/100,2)
        provided=(invoice.tax_details or {}).get('tax_amount')
        if provided is None:
            invoice.tax_details=invoice.tax_details or {}
            invoice.tax_details['tax_amount']=expected
            return {'ok':True,'invoice':invoice}
        if abs(provided-expected)>0.02:
            return {'ok':False,'error':f'Invalid VAT amount: expected {expected}, got {provided}'}
        return {'ok':True,'invoice':invoice}
    if config.get('type')=='GST':
        hsn_map=config.get('hsn_rates',{})
        total_tax=0
        for it in invoice.items or []:
            hsn=str(it.get('hsn'))
            rate=hsn_map.get(hsn)
            if rate is None:
                return {'ok':False,'error':f'HSN {hsn} not found in tax config'}
            total_tax+=round(it.get('qty',1)*it.get('rate',0)*rate/100,2)
        provided=(invoice.tax_details or {}).get('tax_amount')
        if provided is None:
            invoice.tax_details=invoice.tax_details or {}
            invoice.tax_details['tax_amount']=total_tax
            return {'ok':True,'invoice':invoice}
        if abs(provided-total_tax)>0.05:
            return {'ok':False,'error':f'Invalid GST total: expected {total_tax}, got {provided}'}
        return {'ok':True,'invoice':invoice}
    return {'ok':True,'invoice':invoice}
