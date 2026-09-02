"""SQLAlchemy Engine 和请求范围 Session 的边界测试。"""

from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import patch

from app.core.config import Settings
from app.db.session import (
    DatabaseConfigurationError,
    create_database_engine,
    get_database_engine,
    get_db_session,
    get_session_factory,
)


class DatabaseEngineTest(TestCase):
    """验证 Engine 按需创建和数据库配置失败边界。"""

    def tearDown(self) -> None:
        get_session_factory.cache_clear()
        get_database_engine.cache_clear()

    def test_normalizes_postgresql_url_without_connecting(self) -> None:
        engine = create_database_engine(
            "postgresql://user:password@localhost:5432/jack"
        )

        self.assertEqual(engine.url.drivername, "postgresql+asyncpg")
        engine.sync_engine.dispose()

    def test_rejects_database_engine_when_not_configured(self) -> None:
        settings = Settings(_env_file=None)

        with patch("app.db.session.get_settings", return_value=settings):
            with self.assertRaises(DatabaseConfigurationError):
                get_database_engine()


class DatabaseSessionTest(IsolatedAsyncioTestCase):
    """验证 Session 依赖关闭资源并回滚未处理异常。"""

    class FakeSession:
        def __init__(self) -> None:
            self.entered = False
            self.closed = False
            self.rolled_back = False

        async def __aenter__(self) -> "DatabaseSessionTest.FakeSession":
            self.entered = True
            return self

        async def __aexit__(self, *args: object) -> None:
            self.closed = True

        async def rollback(self) -> None:
            self.rolled_back = True

    class FakeSessionFactory:
        def __init__(self, session: "DatabaseSessionTest.FakeSession") -> None:
            self.session = session

        def __call__(self) -> "DatabaseSessionTest.FakeSession":
            return self.session

    async def test_yields_and_closes_request_scope_session(self) -> None:
        session = self.FakeSession()
        factory = self.FakeSessionFactory(session)

        with patch("app.db.session.get_session_factory", return_value=factory):
            received = [item async for item in get_db_session()]

        self.assertEqual(received, [session])
        self.assertTrue(session.entered)
        self.assertTrue(session.closed)
        self.assertFalse(session.rolled_back)

    async def test_rolls_back_when_request_scope_fails(self) -> None:
        session = self.FakeSession()
        factory = self.FakeSessionFactory(session)

        with patch("app.db.session.get_session_factory", return_value=factory):
            dependency = get_db_session()
            self.assertIs(await dependency.__anext__(), session)
            with self.assertRaises(RuntimeError):
                await dependency.athrow(RuntimeError("request failed"))

        self.assertTrue(session.rolled_back)
        self.assertTrue(session.closed)
