from sqlalchemy.ext.asyncio import AsyncSession
from src.app.infrastructure.database.connection import AsyncSessionLocal


class DatabaseSession:
    """Контекстный менеджер для работы с сессиями БД"""

    def __init__(self):
        self.session: AsyncSession = None

    async def __aenter__(self) -> AsyncSession:
        self.session = AsyncSessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()