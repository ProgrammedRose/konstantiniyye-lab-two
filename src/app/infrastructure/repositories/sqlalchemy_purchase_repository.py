from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.domain.entities.purchase import Purchase
from src.app.infrastructure.database.models import PurchaseModel, BookModel


class SQLAlchemyPurchaseRepository(PurchaseRepository):
    """Реализация репозитория покупок на SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Purchase]:
        """Получить все покупки из БД с загрузкой связанных книг"""
        result = await self.session.execute(
            select(PurchaseModel)
            .options(selectinload(PurchaseModel.book))
            .order_by(PurchaseModel.date.desc())
        )
        purchase_models = result.scalars().all()

        purchases = []
        for model in purchase_models:
            # Создаём доменную сущность Book
            book_entity = model.book
            from src.app.domain.entities.book import Book
            book = Book(
                title=book_entity.title,
                author=book_entity.author,
                price=book_entity.price
            )

            # Создаём доменную сущность Purchase
            purchase = Purchase(book=book, quantity=model.quantity)
            purchase.date = model.date  # Сохраняем дату из БД
            purchases.append(purchase)

        return purchases

    async def add(self, purchase: Purchase) -> None:
        """Добавить покупку в БД"""
        # Получаем книгу из БД
        result = await self.session.execute(
            select(BookModel).where(
                (BookModel.title == purchase.book.title) &
                (BookModel.author == purchase.book.author) &
                (BookModel.price == purchase.book.price)
            )
        )
        book_model = result.scalar_one_or_none()

        if not book_model:
            # Если книги нет в БД, создаём её
            book_model = BookModel(
                title=purchase.book.title,
                author=purchase.book.author,
                price=purchase.book.price
            )
            self.session.add(book_model)
            await self.session.flush()

        # Создаём покупку
        purchase_model = PurchaseModel(
            book_id=book_model.id,
            quantity=purchase.quantity,
            total_price=purchase.price,
            date=purchase.date
        )

        self.session.add(purchase_model)
        await self.session.commit()

    async def count(self) -> int:
        """Получить количество покупок в БД"""
        result = await self.session.execute(
            select(func.count(PurchaseModel.id))
        )
        return result.scalar()