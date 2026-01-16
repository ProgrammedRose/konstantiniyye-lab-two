FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей для psycopg2 и grpc tools
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего приложения
COPY . .

# Генерация Python stubs из proto-файлов (gRPC) — выводим в пакет protos
RUN python -m grpc_tools.protoc -I=src/app/grpc/protos --python_out=src/app/grpc/protos --grpc_python_out=src/app/grpc/protos src/app/grpc/protos/*.proto

# Экспорт порта
EXPOSE 8000
EXPOSE 50051

# Команда запуска (миграции, затем запуск сервера)
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.app.main:app --host 0.0.0.0 --port 8000"]