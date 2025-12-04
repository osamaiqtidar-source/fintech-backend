from importlib import import_module
from app.models.models_einvoice import EInvoiceProvider if False else None
from app.utils.secret_store import load_provider_credentials
from app.db import SessionLocal
from app.audit import log_admin_action
def get_providers_for_country(db, country):
    # simple raw query to remain compatible if models not imported
    rows = db.execute("SELECT id, name, country, priority, config, encrypted_credentials_ref FROM einvoice_provider WHERE country = %s AND enabled = true ORDER BY priority ASC", (country,)).fetchall()
    providers = []
    for r in rows:
        providers.append({
            'id': r[0],
            'name': r[1],
            'country': r[2],
            'priority': r[3],
            'config': r[4],
            'ref': r[5]
        })
    return providers
def instantiate_handler(provider):
    cfg = provider.get('config') or {}
    handler_module = cfg.get('handler_module')
    if not handler_module:
        raise RuntimeError('handler_module not configured for provider ' + str(provider.get('id')))
    creds = load_provider_credentials(provider.get('ref')) if provider.get('ref') else {}
    module = import_module(handler_module)
    HandlerClass = getattr(module, 'Handler')
    return HandlerClass(credentials=creds, config=cfg)
def submit_invoice_via_providers(invoice, company):
    db = SessionLocal()
    try:
        providers = get_providers_for_country(db, company.get('country') if isinstance(company, dict) else getattr(company, 'country', None))
        payload = {}  # transform invoice as needed
        for p in providers:
            try:
                handler = instantiate_handler(p)
                res = handler.submit_invoice(invoice)
                # record to einvoice_log
                db.execute("INSERT INTO einvoice_log (invoice_id, provider_id, company_id, request_payload, response_payload, status) VALUES (%s,%s,%s,%s,%s,%s)", (getattr(invoice,'id',None), p['id'], company.get('id') if isinstance(company, dict) else getattr(company,'id',None), payload, res, 'success' if res.get('ok') else 'failed'))
                db.commit()
                if res.get('ok'):
                    return {'ok': True, 'provider': p['name'], 'response': res}
            except Exception as e:
                db.execute("INSERT INTO einvoice_log (invoice_id, provider_id, company_id, request_payload, response_payload, status) VALUES (%s,%s,%s,%s,%s,%s)", (getattr(invoice,'id',None), p['id'], company.get('id') if isinstance(company, dict) else getattr(company,'id',None), payload, {'ok':False,'error':str(e)}, 'failed'))
                db.commit()
                continue
        return {'ok': False, 'error': 'All providers failed'}
    finally:
        db.close()
