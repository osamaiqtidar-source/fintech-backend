import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./local.db')
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
