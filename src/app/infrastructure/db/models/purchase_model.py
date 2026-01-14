# # from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
# # from sqlalchemy.orm import relationship
# # from datetime import datetime
# # from src.app.infrastructure.db.base import Base
# #
# # # ORM модель покупки
# # class PurchaseModel(Base):
# #     __tablename__ = "purchases"
# #
# #     id = Column(Integer, primary_key=True, index=True)
# #     book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
# #     quantity = Column(Integer, nullable=False)
# #     total_price = Column(Numeric(10,2), nullable=False)
# #     date = Column(DateTime, default=datetime.utcnow)
# #
# #     # Связь с книгой
# #     book = relationship("BookModel")
#
# # src/app/infrastructure/db/models/purchase_model.py
# from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
# from sqlalchemy.orm import relationship
# from datetime import datetime
#
# # Импортируем Base из родительского каталога
# from ..base import Base
#
#
# class PurchaseModel(Base):
#     __tablename__ = 'purchases'
#
#     id = Column(Integer, primary_key=True, index=True)
#     book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     total_price = Column(Float, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#
#     # Используем строку для relationship
#     book = relationship("BookModel", backref="purchases")