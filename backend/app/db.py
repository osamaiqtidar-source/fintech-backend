import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from sqlalchemy.exc import OperationalError

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
# INIT DB
# ----------------------------
def init_db():
    try:
        import backend.app.models
        import backend.app.models_extra

        SQLModel.metadata.create_all(engine)
        print("✔ All tables created successfully")
    except Exception as e:
        print("init_db error:", e)


# ----------------------------
# CREATE DYNAMIC SUPER ADMIN
# ----------------------------
def ensure_first_super_admin():
    """Creates dynamic-password super admin if none exists."""
    from backend.app.models import User

    db = SessionLocal()
    try:
        # Check if table exists
        try:
            db.execute('SELECT id FROM "user" LIMIT 1;')
        except Exception:
            print("⚠ User table not ready yet — skipping super_admin creation")
            return

        existing = db.query(User).filter(User.role == "super_admin").first()

        if existing:
            print("✔ Super admin already exists")
            return

        # Create dynamic super admin
        admin = User(
            email="admin@system.local",
            role="super_admin",
            is_dynamic_password=True,
            password_hash=None,   # IMPORTANT
        )

        db.add(admin)
        db.commit()
        print("✔ Created dynamic super_admin (password = DDMMYYYYHH@Saad)")

    except Exception as e:
        print("ensure_first_super_admin failed:", e)
    finally:
        db.close()


# ----------------------------
# RUN ON STARTUP
# ----------------------------
try:
    init_db()
    ensure_first_super_admin()
except Exception as e:
    print("Startup DB init failed:", e)
