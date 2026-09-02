"""SQLAlchemy 异步 Engine 与 Session 的基础设施边界。"""

from collections.abc import AsyncIterator
from functools import lru_cache

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


class DatabaseConfigurationError(RuntimeError):
    """数据库未配置或连接配置无法创建 Engine。"""


def _to_asyncpg_url(database_url: str) -> str:
    """把常见 PostgreSQL URL 统一为 asyncpg 驱动。"""

    if database_url.startswith("postgresql://"):
        return database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
            1,
        )

    return database_url


def create_database_engine(database_url: str) -> AsyncEngine:
    """根据已校验 URL 创建 Engine，但不主动连接数据库。"""

    try:
        return create_async_engine(
            _to_asyncpg_url(database_url),
            pool_pre_ping=True,
        )
    except (ModuleNotFoundError, SQLAlchemyError) as error:
        raise DatabaseConfigurationError(
            "Database engine could not be configured"
        ) from error


@lru_cache(maxsize=1)
def get_database_engine() -> AsyncEngine:
    """按需创建进程级 Engine；未配置时不伪造可用连接。"""

    database_url = get_settings().database_url
    if database_url is None:
        raise DatabaseConfigurationError("Database is not configured")

    return create_database_engine(database_url)


@lru_cache(maxsize=1)
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """为共享 Engine 创建 Session 工厂。"""

    return async_sessionmaker(
        get_database_engine(),
        expire_on_commit=False,
    )


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """提供一个请求范围 Session，并在请求结束后关闭它。"""

    async with get_session_factory()() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def dispose_database_engine() -> None:
    """释放已创建的 Engine，并清理进程级工厂缓存。"""

    if get_database_engine.cache_info().currsize == 0:
        return

    await get_database_engine().dispose()
    get_session_factory.cache_clear()
    get_database_engine.cache_clear()
