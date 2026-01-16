# src/app/infrastructure/repositories/sqlalchemy_user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from src.app.application.ports.user_repository import UserRepository
from src.app.infrastructure.db.models import UserDB
from src.app.domain.entities.user import User


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        user_db = self.db.query(UserDB).filter(UserDB.username == username).first()
        if not user_db:
            return None
        return User(id=user_db.id, username=user_db.username, password_hash=user_db.password_hash, role=user_db.role)

    def add(self, user: User) -> int:
        db_user = UserDB(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user.id

    def get_all(self) -> List[User]:
        users_db = self.db.query(UserDB).all()
        return [User(id=u.id, username=u.username, password_hash=u.password_hash, role=u.role) for u in users_db]

    def get_by_id(self, user_id: int) -> Optional[User]:
        user_db = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user_db:
            return None
        return User(id=user_db.id, username=user_db.username, password_hash=user_db.password_hash, role=user_db.role)

    def delete(self, user_id: int) -> None:
        user_db = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user_db:
            raise IndexError("User not found")
        self.db.delete(user_db)
        self.db.commit()

    def update(self, user_id: int, user: User) -> None:
        user_db = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not user_db:
            raise IndexError("User not found")
        user_db.username = user.username
        user_db.password_hash = user.password_hash
        user_db.role = user.role
        self.db.commit()
