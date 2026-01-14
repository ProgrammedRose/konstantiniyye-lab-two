# test_no_circular.py
import sys

sys.path.insert(0, 'src')

# Создаем Base напрямую
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

print("1. Base created")

# Читаем и выполняем код book_model.py
with open('src/app/infrastructure/db/models/book_model.py', 'r') as f:
    book_code = f.read()

# Заменяем импорт Base на наш локальный Base
book_code = book_code.replace('from ..base import Base', '')
exec(book_code, {'Base': Base, 'Column': __import__('sqlalchemy').Column,
                 'Integer': __import__('sqlalchemy').Integer,
                 'String': __import__('sqlalchemy').String,
                 'DateTime': __import__('sqlalchemy').DateTime,
                 'Float': __import__('sqlalchemy').Float,
                 'datetime': __import__('datetime').datetime})

print("2. BookModel defined")

# То же для purchase_model
with open('src/app/infrastructure/db/models/purchase_model.py', 'r') as f:
    purchase_code = f.read()

purchase_code = purchase_code.replace('from ..base import Base', '')
exec(purchase_code, {'Base': Base, 'Column': __import__('sqlalchemy').Column,
                     'Integer': __import__('sqlalchemy').Integer,
                     'ForeignKey': __import__('sqlalchemy').ForeignKey,
                     'DateTime': __import__('sqlalchemy').DateTime,
                     'Float': __import__('sqlalchemy').Float,
                     'relationship': __import__('sqlalchemy.orm').relationship,
                     'datetime': __import__('datetime').datetime})

print("3. PurchaseModel defined")
print(f"4. Tables in metadata: {list(Base.metadata.tables.keys())}")