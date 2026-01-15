from typing import List, Optional
from sqlalchemy.orm import Session
from src.app.application.ports.book_repository import BookRepository
from src.app.domain.entities.book import Book
from src.app.infrastructure.db.models import BookDB

from sqlalchemy.exc import IntegrityError


class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Book]:
        books_db = self.db.query(BookDB).all()
        return [
            Book(
                id=book.id,  # Передаем ID из БД
                title=book.title,
                author=book.author,
                price=book.price
            ) for book in books_db
        ]

    def get_by_id(self, book_id: int) -> Optional[Book]:
        book_db = self.db.query(BookDB).filter(BookDB.id == book_id).first()
        if not book_db:
            return None
        return Book(
            id=book_db.id,  # Передаем ID из БД
            title=book_db.title,
            author=book_db.author,
            price=book_db.price
        )

    def add(self, book: Book) -> int:
        db_book = BookDB(
            title=book.title,
            author=book.author,
            price=book.price
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book.id

    def update(self, book_id: int, book: Book) -> None:
        db_book = self.db.query(BookDB).filter(BookDB.id == book_id).first()
        if not db_book:
            raise IndexError("Book not found")

        db_book.title = book.title
        db_book.author = book.author
        db_book.price = book.price
        self.db.commit()
        # Обновляем ID в доменной сущности
        book.id = db_book.id

    def delete(self, book_id: int) -> None:
        db_book = self.db.query(BookDB).filter(BookDB.id == book_id).first()
        if not db_book:
            raise IndexError("Book not found")

        try:
            self.db.delete(db_book)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()  # Откатываем транзакцию
            if "foreign key constraint" in str(e).lower():
                raise ValueError(f"Cannot delete book with ID {book_id}. It has associated purchases.")
            raise
