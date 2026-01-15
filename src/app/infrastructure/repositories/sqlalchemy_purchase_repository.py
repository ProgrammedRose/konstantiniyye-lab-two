from typing import List
from sqlalchemy.orm import Session
from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.domain.entities.purchase import Purchase
from src.app.domain.entities.book import Book
from src.app.infrastructure.db.models import PurchaseDB, BookDB


class SQLAlchemyPurchaseRepository(PurchaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Purchase]:
        purchases_db = (
            self.db.query(PurchaseDB)
            .join(BookDB)
            .all()
        )
        return [
            Purchase(
                book=Book(
                    id=p.book.id,  # Передаем ID книги
                    title=p.book.title,
                    author=p.book.author,
                    price=p.book.price
                ),
                quantity=p.quantity,
                date=p.date
            ) for p in purchases_db
        ]

    def add(self, purchase: Purchase) -> None:
        # Ищем книгу по ID
        if purchase.book.id is not None:
            book_db = self.db.query(BookDB).filter(BookDB.id == purchase.book.id).first()
        else:
            # Если ID нет, ищем по названию и автору
            book_db = self.db.query(BookDB).filter(
                BookDB.title == purchase.book.title,
                BookDB.author == purchase.book.author
            ).first()

        # Если книга не найдена, создаем новую
        if not book_db:
            book_db = BookDB(
                title=purchase.book.title,
                author=purchase.book.author,
                price=purchase.book.price
            )
            self.db.add(book_db)
            self.db.commit()
            self.db.refresh(book_db)
            # Обновляем ID в доменной сущности
            purchase.book.id = book_db.id

        db_purchase = PurchaseDB(
            book_id=book_db.id,
            quantity=purchase.quantity,
            total_price=purchase.book.price * purchase.quantity,
            date=purchase.date
        )
        self.db.add(db_purchase)
        self.db.commit()

    def count(self) -> int:
        return self.db.query(PurchaseDB).count()