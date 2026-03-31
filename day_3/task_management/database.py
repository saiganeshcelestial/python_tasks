from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# ── Engine ────────────────────────────────────────────────────────────────────
# pool_size=5        : keep 5 persistent connections alive in the pool
# max_overflow=10    : allow 10 extra connections under spike load
# pool_timeout=30    : raise after 30s if no connection is available
# pool_recycle=1800  : recycle connections every 30 min (Supabase idle-kills them)
# pool_pre_ping=True : health-check a connection before handing it out
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False,
)

# Mask password for safe logging
_parts = DATABASE_URL.split("@")
_display = "postgresql://***@" + _parts[1] if len(_parts) > 1 else DATABASE_URL
print(f"Engine created: {_display}")

# ── Session factory ────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("Session factory ready.")

# ── Declarative base (shared by all ORM models) ────────────────────────────────
Base = declarative_base()


# ── FastAPI dependency ─────────────────────────────────────────────────────────
def get_db():
    """Yields a SQLAlchemy session and guarantees it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Health check ───────────────────────────────────────────────────────────────
def verify_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print(f"Connection verified: SELECT 1 returned {result}")
            print("Database connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")
        raise
