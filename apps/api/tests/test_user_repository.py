"""User ORM Model 与 Repository 的边界测试。"""

from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository


class UserModelTest(TestCase):
    """验证 User 的表名、字段和数据库约束声明。"""

    def test_declares_minimal_user_table_contract(self) -> None:
        table = User.__table__

        self.assertEqual(table.name, "users")
        self.assertIsNotNone(table.c.id.primary_key)
        self.assertEqual(table.c.email.type.length, 320)
        self.assertEqual(table.c.display_name.type.length, 100)
        self.assertTrue(table.c.email.unique)
        self.assertFalse(table.c.email.nullable)
        self.assertFalse(table.c.display_name.nullable)
        self.assertIsNotNone(table.c.created_at.server_default)

    def test_accepts_typed_user_values(self) -> None:
        user_id = uuid4()
        user = User(
            id=user_id,
            email="jack@example.com",
            display_name="Jack",
        )

        self.assertIsInstance(user.id, UUID)
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.email, "jack@example.com")
        self.assertEqual(user.display_name, "Jack")


class UserRepositoryTest(IsolatedAsyncioTestCase):
    """验证 Repository 复用 Session 且不越权管理事务。"""

    def setUp(self) -> None:
        self.session = Mock(spec=AsyncSession)
        self.session.flush = AsyncMock()
        self.session.get = AsyncMock()
        self.session.execute = AsyncMock()
        self.session.commit = AsyncMock()
        self.repository = UserRepository(self.session)

    async def test_add_flushes_without_committing(self) -> None:
        user = User(
            email="jack@example.com",
            display_name="Jack",
        )

        result = await self.repository.add(user)

        self.assertIs(result, user)
        self.session.add.assert_called_once_with(user)
        self.session.flush.assert_awaited_once_with()
        self.session.commit.assert_not_awaited()

    async def test_get_by_id_delegates_to_session(self) -> None:
        user_id = uuid4()
        user = User(
            id=user_id,
            email="jack@example.com",
            display_name="Jack",
        )
        self.session.get.return_value = user

        result = await self.repository.get_by_id(user_id)

        self.assertIs(result, user)
        self.session.get.assert_awaited_once_with(User, user_id)

    async def test_get_by_email_executes_scoped_query(self) -> None:
        user = User(
            email="jack@example.com",
            display_name="Jack",
        )
        query_result = Mock()
        query_result.scalar_one_or_none.return_value = user
        self.session.execute.return_value = query_result

        result = await self.repository.get_by_email("jack@example.com")

        self.assertIs(result, user)
        self.session.execute.assert_awaited_once()
        statement = self.session.execute.await_args.args[0]
        self.assertEqual(statement.whereclause.right.value, "jack@example.com")
        query_result.scalar_one_or_none.assert_called_once_with()
