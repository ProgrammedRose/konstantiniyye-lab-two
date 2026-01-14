from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserCreateSchema(BaseModel):
    """Схема для регистрации пользователя"""
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="secret123")


class UserLoginSchema(BaseModel):
    """Схема для входа пользователя"""
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="secret123")


class TokenSchema(BaseModel):
    """Схема для JWT токена"""
    access_token: str
    token_type: str = "bearer"


class UserReadSchema(BaseModel):
    """Схема для чтения данных пользователя"""
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True