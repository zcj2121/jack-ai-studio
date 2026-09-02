"""用户数据库查询与写入边界。"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """封装 User 的最小数据库操作，不拥有业务事务。"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> User:
        """加入当前事务并 flush，让数据库约束尽早生效。"""

        self._session.add(user)
        await self._session.flush()
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        """按主键查询用户。"""

        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """按唯一邮箱查询用户。"""

        statement = select(User).where(User.email == email)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
