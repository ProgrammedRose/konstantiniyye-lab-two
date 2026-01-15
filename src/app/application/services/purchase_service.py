from typing import List
from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.application.ports.book_repository import BookRepository
from src.app.application.dto.purchase_dto import (
    PurchaseCreateDTO,
    PurchaseReadDTO
)
from src.app.domain.entities.purchase import Purchase
from src.app.domain.rules.purchase_rules import check_max_purchases
from src.app.domain.entities.book import Book

MAX_QUANTITY = 50

class PurchaseService:

    def __init__(
        self,
        purchase_repository: PurchaseRepository,
        book_repository: BookRepository
    ):
        self.purchase_repository = purchase_repository
        self.book_repository = book_repository

    def get_all_purchases(self) -> List[PurchaseReadDTO]:
        purchases = self.purchase_repository.get_all()
        return [
            PurchaseReadDTO(
                book_title=p.book.title,
                quantity=p.quantity,
                total_price=p.book.price * p.quantity,
                date=p.date
            )
            for p in purchases
        ]

    def create_purchase(self, dto: PurchaseCreateDTO) -> None:
        check_max_purchases(self.purchase_repository.count())

        if dto.quantity > MAX_QUANTITY:
            raise ValueError(
                f"Cannot purchase more than {MAX_QUANTITY} items at once"
            )

        book = self.book_repository.get_by_id(dto.book_id)
        if book is None:
            raise ValueError("Book not found")

        # Убедитесь, что у книги есть ID
        if book.id is None:
            raise ValueError("Book ID is missing")

        purchase = Purchase(book=book, quantity=dto.quantity)
        self.purchase_repository.add(purchase)