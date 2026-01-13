# app/web/dependencies.py

from src.app.infrastructure.storage.memory_storage import MemoryStorage
from src.app.infrastructure.repositories.in_memory_book_repository import InMemoryBookRepository
from src.app.infrastructure.repositories.in_memory_purchase_repository import InMemoryPurchaseRepository

from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService


_book_storage = MemoryStorage()
_purchase_storage = MemoryStorage()

_book_repository = InMemoryBookRepository(_book_storage)
_purchase_repository = InMemoryPurchaseRepository(_purchase_storage)


def get_book_service() -> BookService:
    return BookService(_book_repository)


def get_purchase_service() -> PurchaseService:
    return PurchaseService(
        purchase_repository=_purchase_repository,
        book_repository=_book_repository
    )