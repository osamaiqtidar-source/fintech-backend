# AUTO_DB_DRIVER_FIX - ensure psycopg driver available for SQLAlchemy
import os as __os
__DATABASE_URL_RAW = __os.getenv('DATABASE_URL', 'sqlite:///./test.db')
# normalize common postgres URL variants to explicit psycopg3 dialect
if __DATABASE_URL_RAW.startswith('postgres://'):
    __DATABASE_URL = __DATABASE_URL_RAW.replace('postgres://', 'postgresql+psycopg://', 1)
elif __DATABASE_URL_RAW.startswith('postgresql://') and '+psycopg' not in __DATABASE_URL_RAW:
    __DATABASE_URL = __DATABASE_URL_RAW.replace('postgresql://', 'postgresql+psycopg://', 1)
else:
    __DATABASE_URL = __DATABASE_URL_RAW
# export normalized for the rest of the module
try:
    DATABASE_URL = __DATABASE_URL
except Exception:
    pass

# AUTO_DB_DRIVER_FIX_END

import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./test.db')
engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
def init_db():
    from . import models, models_extra
    SQLModel.metadata.create_all(engine)
