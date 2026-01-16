
from typing import List
from src.app.application.ports.book_repository import BookRepository
from src.app.application.dto.book_dto import (
    BookCreateDTO,
    BookUpdateDTO,
    BookReadDTO
)
from src.app.domain.entities.book import Book


# Сервис книжки
# Создает ее, добовляет, удаляет и обновляет книги, и еще есть гетер всех книг.

class BookService:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def get_all_books(self) -> List[BookReadDTO]:
        books = self.repository.get_all()
        return [
            BookReadDTO(
                id=book.id,
                title=book.title,
                author=book.author,
                price=book.price
            )
            for book in books
        ]

    def add_book(self, dto: BookCreateDTO) -> int:
        book = Book(dto.title, dto.author, dto.price)
        return self.repository.add(book)

    def update_book(self, book_id: int, dto: BookUpdateDTO) -> None:
        # For simplicity replace all fields — BookUpdateDTO in this implementation should contain fields
        # (if you want partial update, adapt accordingly)
        book = Book(dto.title, dto.author, dto.price)
        self.repository.update(book_id, book)

    def delete_book(self, book_id: int) -> None:
        self.repository.delete(book_id)
