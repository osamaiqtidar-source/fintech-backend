from fastapi import FastAPI
from .db import init_db
from .routers import auth, admin, invoices, einvoice, connector, admin_settings
app=FastAPI()
@app.on_event('startup')
def start():
    init_db()
app.include_router(auth.router,prefix='/api/v1/auth')
app.include_router(admin.router,prefix='/api/v1/admin')
app.include_router(admin_settings.router,prefix='/api/v1/admin/settings')
app.include_router(invoices.router,prefix='/api/v1/invoices')
app.include_router(einvoice.router,prefix='/api/v1/einvoice')
app.include_router(connector.router,prefix='/api/v1/connector')
@app.get('/health')
def h():
    return {'status':'ok'}
