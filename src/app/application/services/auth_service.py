from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from src.app.application.ports.auth_repository import AuthRepository
from src.app.application.dto.auth_dto import UserCreateDTO, UserLoginDTO, TokenDTO, UserReadDTO
from src.app.domain.entities.user import User
from src.app.infrastructure.auth.password import verify_password, get_password_hash
from src.app.infrastructure.auth.jwt_handler import (
    SECRET_KEY, ALGORITHM, create_access_token
)


class AuthService:
    """Сервис аутентификации"""

    def __init__(self, repository: AuthRepository):
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, dto: UserCreateDTO) -> UserReadDTO:
        """Регистрация нового пользователя"""
        # Проверяем, существует ли пользователь с таким именем
        existing_user = await self.repository.get_by_username(dto.username)
        if existing_user:
            raise ValueError(f"Username {dto.username} already exists")

        # Проверяем, существует ли пользователь с таким email
        existing_email = await self.repository.get_by_email(dto.email)
        if existing_email:
            raise ValueError(f"Email {dto.email} already exists")

        # Хешируем пароль
        hashed_password = get_password_hash(dto.password)

        # Создаём доменную сущность
        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )

        # Сохраняем в БД
        user_id = await self.repository.create_user(user)
        user.id = user_id

        # Возвращаем DTO
        return UserReadDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at
        )

    async def authenticate_user(self, dto: UserLoginDTO) -> Optional[TokenDTO]:
        """Аутентификация пользователя и выдача JWT токена"""
        # Ищем пользователя
        user = await self.repository.get_by_username(dto.username)
        if not user:
            return None

        # Проверяем пароль
        if not verify_password(dto.password, user.hashed_password):
            return None

        # Проверяем активен ли пользователь
        if not user.is_active:
            raise ValueError("User account is disabled")

        # Создаём JWT токен
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )

        return TokenDTO(access_token=access_token)

    async def get_current_user(self, token: str) -> Optional[User]:
        """Получить текущего пользователя по JWT токену"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None

            user = await self.repository.get_by_username(username)
            return user
        except jwt.JWTError:
            return None