# AUTO_DB_DRIVER_PREFERENCE: psycopg2 primary, psycopg3 fallback
import os as __os
__RAW_DB = __os.getenv("DATABASE_URL", "sqlite:///./test.db")
__DB = __RAW_DB.strip()

# Normalize common host prefixes to explicit dialects,
# prefer psycopg2 when the URL has no explicit '+psycopg' suffix.
if __DB.startswith("postgres://"):
    __DB = __DB.replace("postgres://", "postgresql+psycopg2://", 1)
elif __DB.startswith("postgresql://") and "+psycopg" not in __DB:
    __DB = __DB.replace("postgresql://", "postgresql+psycopg2://", 1)

# If user provided postgresql+psycopg (psycopg3) or postgresql+psycopg2, keep as-is.
DATABASE_URL = __DB

# For debugging: expose chosen driver name (not necessary in production)
try:
    if DATABASE_URL.startswith("postgresql+psycopg2"):
        __DRIVER_USED = "psycopg2"
    elif DATABASE_URL.startswith("postgresql+psycopg"):
        __DRIVER_USED = "psycopg3"
    else:
        __DRIVER_USED = "other"
except Exception:
    __DRIVER_USED = "unknown"
# END AUTO_DB_DRIVER_PREFERENCE


import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./test.db')
engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
def init_db():
    from . import models, models_extra
    SQLModel.metadata.create_all(engine)
