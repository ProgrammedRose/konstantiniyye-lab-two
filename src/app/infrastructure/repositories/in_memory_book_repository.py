
from typing import List
from src.app.application.ports.book_repository import BookRepository
from src.app.domain.entities.book import Book
from src.app.infrastructure.storage.memory_storage import MemoryStorage


class InMemoryBookRepository(BookRepository):

    def __init__(self, storage: MemoryStorage):
        self.storage = storage

    def get_all(self) -> List[Book]:
        return self.storage.books.copy()

    def get_by_id(self, book_id: int) -> Book | None:
        try:
            return self.storage.books[book_id]
        except IndexError:
            return None

    def add(self, book: Book) -> int:
        self.storage.books.append(book)
        return len(self.storage.books) - 1

    def update(self, book_id: int, book: Book) -> None:
        if book_id >= len(self.storage.books):
            raise IndexError("Book not found")
        self.storage.books[book_id] = book

    def delete(self, book_id: int) -> None:
        if book_id >= len(self.storage.books):
            raise IndexError("Book not found")
        del self.storage.books[book_id]
