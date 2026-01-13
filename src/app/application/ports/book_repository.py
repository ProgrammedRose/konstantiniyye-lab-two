
from abc import ABC, abstractmethod
from typing import List
from src.app.domain.entities.book import Book


# Абстрактный класс, типо интерфейс, с абстрактными методами
# Реализуем в сервисах (см ниже)
class BookRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Book]:
        pass

    @abstractmethod
    def get_by_id(self, book_id: int) -> Book | None:
        pass

    @abstractmethod
    def add(self, book: Book) -> int:
        pass

    @abstractmethod
    def update(self, book_id: int, book: Book) -> None:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> None:
        pass
