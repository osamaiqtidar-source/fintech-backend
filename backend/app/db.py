import os
import logging

# FIX: declarative_base comes from sqlalchemy.orm now
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.context import CryptContext
from sqlalchemy.exc import OperationalError

Base = declarative_base()

# Silence SQLAlchemy logs
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)

# ----------------------------
# DATABASE URL FIXER (Render Safe)
# ----------------------------
raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db").strip()

if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("postgresql://") and "+psycopg2" not in raw_url:
    raw_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

DATABASE_URL = raw_url

# ----------------------------
# ENGINE + SESSION
# ----------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------------------
# INIT DB (CREATE ALL TABLES)
# ----------------------------
def init_db():
    try:
        # FIX: correct imports
        import backend.app.models
        import backend.app.company_extra

        SQLModel.metadata.create_all(engine)
        print("✔ All tables created successfully")
    except Exception as e:
        print("init_db error:", e)

# ----------------------------
# CREATE FIRST SUPER ADMIN
# ----------------------------
def ensure_first_super_admin():
    from backend.app.user import User

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.role == "super_admin").first()

        if existing:
            print("✔ Super admin already exists")
            return

        admin = User(
            email="admin@system.local",
            role="super_admin",
            is_dynamic_password=True,
            password_hash=None
        )

        db.add(admin)
        db.commit()
        print("✔ Created dynamic super_admin (password = DDMMYYYYHH@Saad)")

    except OperationalError as e:
        print("Database not ready:", e)
    except Exception as e:
        print("ensure_first_super_admin failed:", e)
    finally:
        db.close()
