# src/app/infrastructure/db/seed.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

from .models import BookDB, Base, UserDB
from .session import engine
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            print("Тестовые книги успешно добавлены")
        else:
            print("Тестовые книги уже существуют в базе")

        # Users
        if db.query(UserDB).count() == 0:
            print("Добавление тестовых пользователей...")
            admin_password_hash = pwd_context.hash("admin")
            user_password_hash = pwd_context.hash("user")
            admin = UserDB(username="admin", password_hash=admin_password_hash, role="admin")
            user = UserDB(username="user", password_hash=user_password_hash, role="user")
            db.add_all([admin, user])
            db.commit()
            print("Тестовые пользователи успешно добавлены")
        else:
            print("Пользователи уже существуют в базе")

    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
