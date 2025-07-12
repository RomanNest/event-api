import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from alembic import context
import os
from dotenv import load_dotenv

from app.database import Base  # Base = declarative_base()
from app.models import User, Event, Booking  # щоб Alembic "побачив" таблиці


# Load .env
load_dotenv()

# Alembic Config object
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Get DB URL from env
DATABASE_URL = os.getenv("DATABASE_URL")

target_metadata = Base.metadata


def run_migrations_offline():
    """Offline mode"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, future=True)

    async def run_migrations():
        async with connectable.connect() as connection:
            def do_run_migrations(conn):
                context.configure(connection=conn, target_metadata=target_metadata)
                with context.begin_transaction():
                    context.run_migrations()

            await connection.run_sync(do_run_migrations)

    asyncio.run(run_migrations())



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
