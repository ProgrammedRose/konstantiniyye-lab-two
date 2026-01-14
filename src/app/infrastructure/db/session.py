# Тут настройка сессии и подключения к PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config.settings import settings

DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Создаем движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # для логов SQL-запросов
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
