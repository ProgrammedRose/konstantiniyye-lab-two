from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserCreateDTO:
    """DTO для создания пользователя"""
    username: str
    email: str
    password: str


@dataclass
class UserLoginDTO:
    """DTO для входа пользователя"""
    username: str
    password: str


@dataclass
class TokenDTO:
    """DTO для JWT токена"""
    access_token: str
    token_type: str = "bearer"


@dataclass
class UserReadDTO:
    """DTO для чтения данных пользователя"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime