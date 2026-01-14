# test_fix.py
import sys
import os

# Добавляем путь к src
sys.path.insert(0, 'src')

# Импортируем Base (пустой, без моделей)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Проверяем что metadata пустая
print(f"Tables before importing models: {list(Base.metadata.tables.keys())}")

# Импортируем модели отдельно
try:
    from app.infrastructure.db.models.book_model import BookModel
    print(f"✓ Imported BookModel")
    print(f"  BookModel.__table__: {BookModel.__table__}")
except Exception as e:
    print(f"✗ Error importing BookModel: {e}")

try:
    from app.infrastructure.db.models.purchase_model import PurchaseModel
    print(f"✓ Imported PurchaseModel")
    print(f"  PurchaseModel.__table__: {PurchaseModel.__table__}")
except Exception as e:
    print(f"✗ Error importing PurchaseModel: {e}")

# Проверяем таблицы в metadata
print(f"\nTables after importing models: {list(Base.metadata.tables.keys())}")