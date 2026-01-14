import asyncio
import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.infrastructure.database.models import Base, BookModel, PurchaseModel, UserModel
from src.app.infrastructure.database.config import db_settings
from src.app.infrastructure.auth.password import get_password_hash

fake = Faker()


async def seed_database():
    """Заполнить базу данных тестовыми данными"""

    # Создаём движок
    engine = create_async_engine(db_settings.database_url)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            print("🌱 Начинаем заполнение базы данных тестовыми данными...")

            # Очищаем таблицы (в обратном порядке из-за foreign keys)
            await session.execute(PurchaseModel.__table__.delete())
            await session.execute(BookModel.__table__.delete())
            await session.execute(UserModel.__table__.delete())
            await session.commit()

            print("🗑️  Старые данные удалены")

            # 1. Создаём тестовых пользователей
            users = []
            for i in range(5):
                user = UserModel(
                    username=f"user_{i + 1}",
                    email=f"user{i + 1}@example.com",
                    hashed_password=get_password_hash(f"password{i + 1}"),
                    is_active=1,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                users.append(user)
                session.add(user)

            # Администратор
            admin = UserModel(
                username="admin",
                email="admin@bookstore.com",
                hashed_password=get_password_hash("admin123"),
                is_active=1,
                created_at=datetime.utcnow() - timedelta(days=60)
            )
            users.append(admin)
            session.add(admin)

            await session.flush()
            print(f"👥 Создано {len(users)} пользователей")

            # 2. Создаём книги
            books = []
            book_titles = [
                "Clean Code", "Design Patterns", "The Pragmatic Programmer",
                "Refactoring", "Domain-Driven Design", "Introduction to Algorithms",
                "Code Complete", "The Mythical Man-Month", "Head First Design Patterns",
                "The Clean Coder", "Working Effectively with Legacy Code",
                "Patterns of Enterprise Application Architecture", "Test Driven Development",
                "The Art of Computer Programming", "Structure and Interpretation of Computer Programs"
            ]

            for i, title in enumerate(book_titles):
                book = BookModel(
                    title=title,
                    author=fake.name(),
                    price=round(random.uniform(10.0, 100.0), 2)
                )
                books.append(book)
                session.add(book)

            await session.flush()
            print(f"📚 Создано {len(books)} книг")

            # 3. Создаём покупки
            purchases = []
            for _ in range(20):
                book = random.choice(books)
                purchase = PurchaseModel(
                    book_id=book.id,
                    quantity=random.randint(1, 5),
                    total_price=book.price * random.randint(1, 5),
                    date=datetime.utcnow() - timedelta(days=random.randint(1, 90))
                )
                purchases.append(purchase)
                session.add(purchase)

            await session.flush()
            print(f"🛒 Создано {len(purchases)} покупок")

            # Фиксируем изменения
            await session.commit()
            print("✅ Тестовые данные успешно добавлены в базу данных!")

            # Выводим информацию
            print("\n📊 Статистика:")
            print(f"   Пользователи: {len(users)}")
            print(f"   Книги: {len(books)}")
            print(f"   Покупки: {len(purchases)}")

            print("\n🔑 Тестовые учетные записи:")
            print("   admin / admin123")
            print("   user_1 / password1")
            print("   user_2 / password2")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при заполнении базы данных: {e}")
            raise
        finally:
            await session.close()
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())