from sqlalchemy.ext.declarative import declarative_base

# базовый класс для SQLAlchemy
Base = declarative_base()

# Импортируем все модели здесь, чтобы они регистрировались в метаданных
from .models.book_model import BookModel
from .models.purchase_model import PurchaseModel