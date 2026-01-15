from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from .models import BookDB, Base
from .session import engine

load_dotenv()


def seed_database():
    """Загружает тестовые данные в базу при запуске приложения"""
    db = Session(engine)

    try:
        # Проверяем, есть ли уже данные
        if db.query(BookDB).count() == 0:
            print("Добавление тестовых данных...")
            seed_books = [
                BookDB(title="Clean Code", author="Robert C. Martin", price=29.99),
                BookDB(title="The Pragmatic Programmer", author="David Thomas", price=35.50),
                BookDB(title="Design Patterns", author="Erich Gamma", price=45.00),
            ]
            db.add_all(seed_books)
            db.commit()
            print("Тестовые данные успешно добавлены")
        else:
            print("Тестовые данные уже существуют в базе")

    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()