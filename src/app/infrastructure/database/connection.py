from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.app.infrastructure.database.config import db_settings

# Создаём асинхронный движок
engine = create_async_engine(
    db_settings.database_url,
    echo=True,  # Логировать SQL-запросы (отключить в продакшене)
    future=True,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncSession:
    """
    Dependency для получения сессии БД.
    Используется в FastAPI Depends.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()