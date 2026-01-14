from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.app.infrastructure.database.connection import get_db_session
from src.app.infrastructure.repositories.sqlalchemy_book_repository import SQLAlchemyBookRepository
from src.app.infrastructure.repositories.sqlalchemy_purchase_repository import SQLAlchemyPurchaseRepository
from src.app.infrastructure.repositories.sqlalchemy_auth_repository import SQLAlchemyAuthRepository

from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService
from src.app.application.services.auth_service import AuthService


# Зависимости для репозиториев
async def get_book_repository(db: AsyncSession = Depends(get_db_session)) -> SQLAlchemyBookRepository:
    return SQLAlchemyBookRepository(db)


async def get_purchase_repository(db: AsyncSession = Depends(get_db_session)) -> SQLAlchemyPurchaseRepository:
    return SQLAlchemyPurchaseRepository(db)


async def get_auth_repository(db: AsyncSession = Depends(get_db_session)) -> SQLAlchemyAuthRepository:
    return SQLAlchemyAuthRepository(db)


# Зависимости для сервисов
async def get_book_service(
    repository: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> BookService:
    return BookService(repository)


async def get_purchase_service(
    purchase_repository: SQLAlchemyPurchaseRepository = Depends(get_purchase_repository),
    book_repository: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> PurchaseService:
    return PurchaseService(purchase_repository, book_repository)


async def get_auth_service(
    repository: SQLAlchemyAuthRepository = Depends(get_auth_repository)
) -> AuthService:
    return AuthService(repository)


# Общая зависимость для БД
get_db = get_db_session