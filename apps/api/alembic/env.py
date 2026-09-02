"""Alembic 的同步/异步 Migration 运行边界。"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import create_database_engine
from app.models import User  # noqa: F401  # 注册 Model 到 Base.metadata


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url() -> str:
    """读取已校验的 PostgreSQL URL，供 offline/online 共用。"""

    database_url = get_settings().database_url
    if database_url is None:
        raise RuntimeError(
            "JACK_DATABASE_URL is required for Alembic migrations"
        )
    return database_url


def run_migrations_offline() -> None:
    """只生成 SQL，不建立数据库连接。"""

    context.configure(
        url=get_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """在同步连接回调中执行 Alembic Migration。"""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """复用项目 AsyncEngine 执行 online Migration。"""

    connectable = create_database_engine(get_database_url())

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """启动异步 Migration 生命周期。"""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
