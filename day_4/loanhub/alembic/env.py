import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# Path setup (so imports work)
# ─────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# ─────────────────────────────────────────────
# Alembic Config
# ─────────────────────────────────────────────
config = context.config

# Get DB URL from .env
db_url = os.getenv("DATABASE_URL")
print("DB URL:", db_url)  # debug (remove later)

# Escape % for Alembic
config.set_main_option("sqlalchemy.url", db_url.replace("%", "%%"))

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─────────────────────────────────────────────
# Import models
# ─────────────────────────────────────────────
from database import Base
from models.db_models import User, Loan  # import ALL models here

target_metadata = Base.metadata


# ─────────────────────────────────────────────
# ✅ FILTER: Only include loanhub schema
# ─────────────────────────────────────────────
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        return object.schema == "loanhub"
    return True


# ─────────────────────────────────────────────
# Offline migrations
# ─────────────────────────────────────────────
def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema="loanhub",
        include_object=include_object,  # ✅ important
    )

    with context.begin_transaction():
        context.run_migrations()


# ─────────────────────────────────────────────
# Online migrations
# ─────────────────────────────────────────────
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema="loanhub",
            include_object=include_object,  # ✅ important
        )

        with context.begin_transaction():
            context.run_migrations()


# ─────────────────────────────────────────────
# Run migrations
# ─────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
