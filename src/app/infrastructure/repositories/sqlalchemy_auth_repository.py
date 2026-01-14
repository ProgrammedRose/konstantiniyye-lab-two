from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.ports.auth_repository import AuthRepository
from src.app.domain.entities.user import User
from src.app.infrastructure.database.models import UserModel


class SQLAlchemyAuthRepository(AuthRepository):
    """Реализация репозитория аутентификации на SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[User]:
        """Найти пользователя по имени"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=bool(model.is_active)
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=bool(model.is_active)
        )

    async def create_user(self, user: User) -> int:
        """Создать нового пользователя"""
        user_model = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=1 if user.is_active else 0
        )

        self.session.add(user_model)
        await self.session.flush()
        await self.session.refresh(user_model)

        return user_model.id