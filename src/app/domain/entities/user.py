from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Доменная сущность Пользователь"""
    id: int = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    is_active: bool = True
    created_at: datetime = None

    def __post_init__(self):
        """Валидация при создании"""
        if not self.username.strip():
            raise ValueError("Username cannot be empty")

        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email format")

        if not self.hashed_password:
            raise ValueError("Password cannot be empty")

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"