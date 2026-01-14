# Тут: URL PostgreSQL
# логин/пароль
# настройки окружения

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "bookstore"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

settings = Settings()