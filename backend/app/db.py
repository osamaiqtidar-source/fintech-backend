import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from sqlalchemy.exc import OperationalError

# ----------------------------
# DATABASE URL FIXER (Render Safe)
# ----------------------------
raw_url = os.getenv("DATABASE_URL", "sqlite:///./test.db").strip()

# Convert postgres:// → postgresql+psycopg2://
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("postgresql://") and "+psycopg" not in raw_url:
    raw_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)

DATABASE_URL = raw_url

# ----------------------------
# ENGINE
# ----------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------------------------------
# INIT DB (CREATE ALL TABLES) — IMPORTANT FIX
# -------------------------------------------------------
def init_db():
    try:
        # Import ALL models so SQLModel registers tables
        import backend.app.models
        import backend.app.models_extra

        SQLModel.metadata.create_all(engine)
        print("✔ All tables created successfully")
    except Exception as e:
        print("init_db error:", e)


# -------------------------------------------------------
# AUTO CREATE FIRST SUPER ADMIN (if none exists)
# -------------------------------------------------------
def ensure_first_super_admin():
    """Create default super_admin ONLY if table exists AND no super_admin present."""
    from backend.app.models import User  # Now correct path

    try:
        db = SessionLocal()

        # Check if "role" column exists OR table exists
        try:
            db.execute("SELECT role FROM \"user\" LIMIT 1;")
        except Exception:
            print("⚠ User table not ready yet — skipping super_admin creation")
            return

        existing = db.query(User).filter(User.role == "super_admin").first()

        if not existing:
            admin = User(
                email="admin@system.local",
                password_hash=pwd_context.hash("Admin@123"),
                role="super_admin"
            )
            db.add(admin)
            db.commit()
            print("✔ Created super_admin: admin@system.local / Admin@123")

    except OperationalError as e:
        print("Database not ready:", e)
    except Exception as e:
        print("ensure_first_super_admin failed:", e)
    finally:
        db.close()


# Automatically run at startup
try:
    init_db()
    ensure_first_super_admin()
except Exception as e:
    print("Startup DB init failed:", e)
