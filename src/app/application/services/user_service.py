# src/app/application/services/user_service.py
from typing import List, Optional
from src.app.application.ports.user_repository import UserRepository
from src.app.application.dto.user_dto import UserCreateDTO, UserReadDTO
from src.app.domain.entities.user import User
from src.app.application.services.auth_service import AuthService


class UserService:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def create_user(self, dto: UserCreateDTO, allow_role_setting: bool = False) -> int:
        # allow_role_setting: only admin allowed to set role. registration sets role 'user'
        role = dto.role if (allow_role_setting and dto.role in ("admin", "user")) else "user"
        password_hash = self.auth_service.hash_password(dto.password)
        user = User(username=dto.username, password_hash=password_hash, role=role)
        return self.user_repository.add(user)

    def get_all_users(self) -> List[UserReadDTO]:
        users = self.user_repository.get_all()
        return [UserReadDTO(id=u.id, username=u.username, role=u.role) for u in users]

    def get_user_by_username(self, username: str) -> Optional[UserReadDTO]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        return UserReadDTO(id=user.id, username=user.username, role=user.role)

    def delete_user(self, user_id: int) -> None:
        self.user_repository.delete(user_id)
