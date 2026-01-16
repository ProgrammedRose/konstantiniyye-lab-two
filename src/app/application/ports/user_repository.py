# src/app/application/ports/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def add(self, user: User) -> int:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def update(self, user_id: int, user: User) -> None:
        pass
