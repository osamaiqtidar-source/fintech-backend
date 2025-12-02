import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///./test.db')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    try:
        from . import models
        SQLModel.metadata.create_all(engine)
    except Exception:
        pass

# FIRST_SUPER_ADMIN_CREATED - injected by backend_v16 generator
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def ensure_first_super_admin():
    try:
        from .models import User
        db = SessionLocal()
        existing = db.query(User).filter(getattr(User, 'role', None) == 'super_admin').first()
        if not existing:
            admin = User(email='admin@system.local', password_hash=pwd_context.hash('Admin@123'), role='super_admin')
            db.add(admin)
            db.commit()
            print('✔ First super_admin created')
    except Exception:
        pass
    finally:
        try:
            db.close()
        except Exception:
            pass

try:
    ensure_first_super_admin()
except Exception:
    pass
