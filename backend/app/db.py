# backend.app.db - database engine and init
import os
from sqlmodel import SQLModel, create_engine, Field, SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func
from passlib.context import CryptContext

# AUTO_DB_DRIVER_PREFERENCE: psycopg2 primary, psycopg3 fallback
__RAW_DB = os.getenv('DATABASE_URL', 'sqlite:///./test.db').strip()
__DB = __RAW_DB
if __DB.startswith('postgres://'):
    __DB = __DB.replace('postgres://', 'postgresql+psycopg2://', 1)
elif __DB.startswith('postgresql://') and '+psycopg' not in __DB:
    __DB = __DB.replace('postgresql://', 'postgresql+psycopg2://', 1)
DATABASE_URL = __DB
# END AUTO_DB_DRIVER_PREFERENCE

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    try:
        from backend.app import models, models_extra
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print('init_db error:', e)

# FIRST_SUPER_ADMIN_CREATED - auto create a default super admin if none exists
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def ensure_first_super_admin():
    try:
        from backend.app.models import User
        db = SessionLocal()
        try:
            existing = db.query(User).filter(getattr(User, 'role', None) == 'super_admin').first()
            if not existing:
                admin = User(email='admin@system.local', password_hash=pwd_context.hash('Admin@123'), role='super_admin')
                db.add(admin)
                db.commit()
                print('✔ First super_admin created: admin@system.local / Admin@123')
        finally:
            db.close()
    except Exception as e:
        print('ensure_first_super_admin failed:', e)

try:
    ensure_first_super_admin()
except Exception:
    pass
