import os
from fastapi import FastAPI
from .db import init_db
from .routers import auth, users, operations, connector, sync, admin, app_updates
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import schedule_periodic_tasks

app = FastAPI(title='Fintech Backend (Production Scaffold)')

@app.on_event('startup')
def on_startup():
    init_db()
    schedule_periodic_tasks()

app.include_router(auth.router, prefix='/api/v1/auth', tags=['auth'])
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])
app.include_router(operations.router, prefix='/api/v1/companies', tags=['operations'])
app.include_router(connector.router, prefix='/api/v1/companies', tags=['connector'])
app.include_router(sync.router, prefix='/api/v1/companies', tags=['sync'])
app.include_router(admin.router, prefix='/api/v1/admin', tags=['admin'])
app.include_router(app_updates.router, prefix='/api/v1/companies', tags=['app_updates'])
