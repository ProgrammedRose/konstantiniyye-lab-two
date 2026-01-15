from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.application.ports.book_repository import BookRepository
from src.app.domain.entities.book import Book
from src.app.infrastructure.database.models import BookModel


class SQLAlchemyBookRepository(BookRepository):
    """Реализация репозитория книг на SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Book]:
        """Получить все книги из БД"""
        result = await self.session.execute(select(BookModel))
        book_models = result.scalars().all()

        # Преобразуем модели SQLAlchemy в доменные сущности
        return [
            Book(
                title=model.title,
                author=model.author,
                price=model.price
            ) for model in book_models
        ]

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        """Получить книгу по ID"""
        result = await self.session.execute(
            select(BookModel).where(BookModel.id == book_id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return Book(
            title=model.title,
            author=model.author,
            price=model.price
        )

    async def add(self, book: Book) -> int:
        """Добавить книгу в БД и вернуть её ID"""
        book_model = BookModel(
            title=book.title,
            author=book.author,
            price=book.price
        )

        self.session.add(book_model)
        await self.session.flush()
        await self.session.refresh(book_model)
        await self.session.commit()

        return book_model.id

    async def update(self, book_id: int, book: Book) -> None:
        """Обновить книгу в БД"""
        stmt = (
            update(BookModel)
            .where(BookModel.id == book_id)
            .values(
                title=book.title,
                author=book.author,
                price=book.price
            )
        )

        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, book_id: int) -> None:
        """Удалить книгу из БД"""
        stmt = delete(BookModel).where(BookModel.id == book_id)
        await self.session.execute(stmt)
        await self.session.commit()