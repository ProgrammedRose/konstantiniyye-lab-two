# src.app/web/dependencies.py
from fastapi import Depends
from src.app.infrastructure.db.session import get_db
from src.app.infrastructure.repositories.sqlalchemy_book_repository import SQLAlchemyBookRepository
from src.app.infrastructure.repositories.sqlalchemy_purchase_repository import SQLAlchemyPurchaseRepository
from src.app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService
from src.app.application.services.auth_service import AuthService
from src.app.application.services.user_service import UserService
from sqlalchemy.orm import Session


def get_book_repository(db: Session = Depends(get_db)):
    return SQLAlchemyBookRepository(db)


def get_purchase_repository(db: Session = Depends(get_db)):
    return SQLAlchemyPurchaseRepository(db)


def get_user_repository(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    repository = get_book_repository(db)
    return BookService(repository)


def get_purchase_service(db: Session = Depends(get_db)) -> PurchaseService:
    book_repository = get_book_repository(db)
    purchase_repository = get_purchase_repository(db)
    return PurchaseService(purchase_repository, book_repository)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repo = get_user_repository(db)
    return AuthService(user_repo)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = get_user_repository(db)
    auth_svc = get_auth_service(db)
    return UserService(user_repo, auth_svc)


# admin-specific instance for dependency injection (so role-restricted endpoints can use a prewired service)
def get_user_service_admin(db: Session = Depends(get_db)) -> UserService:
    user_repo = get_user_repository(db)
    auth_svc = get_auth_service(db)
    return UserService(user_repo, auth_svc)
