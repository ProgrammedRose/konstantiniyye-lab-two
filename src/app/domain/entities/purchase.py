
from datetime import datetime
from src.app.domain.entities.book import Book

class Purchase:
    def __init__(self, book: Book, quantity: int = 1):
        if not isinstance(book, Book):
            raise TypeError("Purchase must contain a Book entity")
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1")

        self.book = book
        self.quantity = quantity
        self.price = book.price * quantity
        self.date = datetime.now()

    def __repr__(self):
        return (
            f"Purchase(book={self.book}, "
            f"quantity={self.quantity}, price={self.price}, date={self.date.isoformat()})"
        )
