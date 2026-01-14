from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class BookModel(Base):
    """Модель SQLAlchemy для таблицы книг"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Связь с покупками
    purchases = relationship("PurchaseModel", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"BookModel(id={self.id}, title='{self.title}', author='{self.author}')"


class PurchaseModel(Base):
    """Модель SQLAlchemy для таблицы покупок"""
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Связи
    book = relationship("BookModel", back_populates="purchases")

    def __repr__(self):
        return f"PurchaseModel(id={self.id}, book_id={self.book_id}, quantity={self.quantity})"


class UserModel(Base):
    """Модель SQLAlchemy для таблицы пользователей (аутентификация)"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1, nullable=False)  # 1 = active, 0 = inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"UserModel(id={self.id}, username='{self.username}', email='{self.email}')"