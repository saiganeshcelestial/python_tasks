import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────
# Add project root to path
# ─────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env
load_dotenv()

# ─────────────────────────────────────────────────────────────
# Alembic Config
# ─────────────────────────────────────────────────────────────
config = context.config

# Override DB URL from .env
db_url = os.getenv("DATABASE_URL").replace("%", "%%")
config.set_main_option("sqlalchemy.url", db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ─────────────────────────────────────────────────────────────
# Import Models (IMPORTANT)
# ─────────────────────────────────────────────────────────────
from database import Base
from models.db_models import User, Task  # register models

target_metadata = Base.metadata

# ─────────────────────────────────────────────────────────────
# OFFLINE MODE
# ─────────────────────────────────────────────────────────────
def include_object(object, name, type_, reflected, compare_to):
    """Exclude objects from schemas we don't manage."""
    if type_ == "table":
        # Only include tables from task_management schema
        schema = object.schema if hasattr(object, 'schema') else None
        return schema == "task_management"
    return True  # Include all other object types


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=["task_management"],
        version_table_schema="task_management",
        include_object=include_object,
        compare_type=False,
        compare_server_default=False
    )

    with context.begin_transaction():
        context.run_migrations()


# ─────────────────────────────────────────────────────────────
# ONLINE MODE
# ─────────────────────────────────────────────────────────────
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=["task_management"],
            version_table_schema="task_management",
            include_object=include_object,
            compare_type=False,
            compare_server_default=False
        )

        with context.begin_transaction():
            context.run_migrations()


# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()