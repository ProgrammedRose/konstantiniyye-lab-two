
MAX_QUANTITY = 50 # по органичению условия

# Сервис покупок (создать покупку и посмотреть все покупки)

from typing import List
from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.application.ports.book_repository import BookRepository
from src.app.application.dto.purchase_dto import (
    PurchaseCreateDTO,
    PurchaseReadDTO
)
from src.app.domain.entities.purchase import Purchase
from src.app.domain.rules.purchase_rules import check_max_purchases



class PurchaseService:
    """Сервис покупок (асинхронный)"""

    def __init__(
            self,
            purchase_repository: PurchaseRepository,
            book_repository: BookRepository
    ):
        self.purchase_repository = purchase_repository
        self.book_repository = book_repository

    async def get_all_purchases(self) -> List[PurchaseReadDTO]:
        purchases = await self.purchase_repository.get_all()
        return [
            PurchaseReadDTO(
                book_title=p.book.title,
                quantity=p.quantity,
                total_price=p.book.price * p.quantity,
                date=p.date
            )
            for p in purchases
        ]

    async def create_purchase(self, dto: PurchaseCreateDTO) -> None:
        # Проверяем максимальное количество покупок
        purchase_count = await self.purchase_repository.count()
        check_max_purchases(purchase_count)

        # Проверяем лимит количества
        if dto.quantity > MAX_QUANTITY:
            raise ValueError(
                f"Cannot purchase more than {MAX_QUANTITY} items at once"
            )

        # Получаем книгу
        book = await self.book_repository.get_by_id(dto.book_id)
        if book is None:
            raise ValueError("Book not found")

        # Создаём покупку
        purchase = Purchase(book, dto.quantity)
        await self.purchase_repository.add(purchase)