from sqlalchemy.orm import Session
from typing import List
from src.app.application.ports.book_repository import BookRepository
from src.app.domain.entities.book import Book
from src.app.application.dto.book_dto import BookCreateDTO, BookUpdateDTO
from src.app.infrastructure.db.models.book_model import BookModel


# Репозиторий книг
class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Book]:
        books = self.db.query(BookModel).all()
        return [Book(id=b.id, title=b.title, author=b.author, price=float(b.price)) for b in books]

    def get_by_id(self, book_id: int) -> Book | None:
        b = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if b:
            return Book(id=b.id, title=b.title, author=b.author, price=float(b.price))
        return None

    def add(self, dto: BookCreateDTO) -> int:
        book = BookModel(title=dto.title, author=dto.author, price=dto.price)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book.id

    def update(self, book_id: int, dto: BookUpdateDTO) -> None:
        book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if not book:
            raise IndexError("Book not found")
        if dto.title is not None:
            book.title = dto.title
        if dto.author is not None:
            book.author = dto.author
        if dto.price is not None:
            book.price = dto.price
        self.db.commit()

    def delete(self, book_id: int) -> None:
        book = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        if not book:
            raise IndexError("Book not found")
        self.db.delete(book)
        self.db.commit()
