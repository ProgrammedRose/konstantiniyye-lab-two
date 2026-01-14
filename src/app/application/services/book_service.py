
# Сервис книжки
# Создает ее, добовляет, удаляет и обновляет книги, и еще есть гетер всех книг.

from typing import List
from src.app.application.ports.book_repository import BookRepository
from src.app.application.dto.book_dto import (
    BookCreateDTO,
    BookUpdateDTO,
    BookReadDTO
)
from src.app.domain.entities.book import Book


class BookService:
    """Сервис книг (асинхронный)"""

    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def get_all_books(self) -> List[BookReadDTO]:
        books = await self.repository.get_all()
        return [
            BookReadDTO(
                id=i,
                title=book.title,
                author=book.author,
                price=book.price
            )
            for i, book in enumerate(books)
        ]

    async def add_book(self, dto: BookCreateDTO) -> int:
        book = Book(dto.title, dto.author, dto.price)
        return await self.repository.add(book)

    async def update_book(self, book_id: int, dto: BookUpdateDTO) -> None:
        book = Book(dto.title, dto.author, dto.price)
        await self.repository.update(book_id, book)

    async def delete_book(self, book_id: int) -> None:
        await self.repository.delete(book_id)

    async def get_book_by_id(self, book_id: int) -> BookReadDTO:
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book with id {book_id} not found")

        return BookReadDTO(
            id=book_id,
            title=book.title,
            author=book.author,
            price=book.price
        )