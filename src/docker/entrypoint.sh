#!/bin/bash

set -e

echo "🚀 Запуск приложения Bookstore..."

# Ждём пока PostgreSQL будет готов (если используется)
if [ "$WAIT_FOR_DB" = "true" ]; then
    echo "⏳ Ожидание PostgreSQL..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
        sleep 1
    done
    echo "✅ PostgreSQL готов!"
fi

# Применяем миграции
echo "📦 Применяем миграции базы данных..."
alembic upgrade head

# Заполняем базу тестовыми данными (если нужно)
if [ "$SEED_DATABASE" = "true" ]; then
    echo "🌱 Заполняем базу тестовыми данными..."
    #python -m scripts.seed
fi

# Запускаем приложение
echo "🚀 Запускаем FastAPI приложение..."
exec uvicorn src.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info