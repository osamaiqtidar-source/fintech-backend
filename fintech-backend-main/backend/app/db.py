import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./test.db')
engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
def init_db():
    from . import models, models_extra
    SQLModel.metadata.create_all(engine)
