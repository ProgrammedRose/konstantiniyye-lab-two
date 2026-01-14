# # from sqlalchemy import Column, Integer, String, Numeric, DateTime
# # from datetime import datetime
# # from src.app.infrastructure.db.base import Base
# #
# #
# # # ORM модель книги
# # class BookModel(Base):
# #     __tablename__ = "books"
# #
# #     id = Column(Integer, primary_key=True, index=True)
# #     title = Column(String, nullable=False)
# #     author = Column(String, nullable=False)
# #     price = Column(Numeric(10, 2), nullable=False)
# #     created_at = Column(DateTime, default=datetime.utcnow)
# #     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
# # src/app/infrastructure/db/models/book_model.py
# from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
#
# # Импортируем Base из того же пакета
# from ..base import Base
#
#
# class BookModel(Base):
#     __tablename__ = 'books'
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     author = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     # Опционально: если есть связи
#     # purchases = relationship("PurchaseModel", back_populates="book")