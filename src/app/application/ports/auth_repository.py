from abc import ABC, abstractmethod
from typing import Optional
from src.app.domain.entities.user import User


class AuthRepository(ABC):
    """Абстрактный порт для репозитория аутентификации"""

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> int:
        pass