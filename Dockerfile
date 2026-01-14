FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src .

# Создаём папку для логов
RUN mkdir -p /var/log/app

# Делаем скрипты исполняемыми
RUN chmod +x /app/docker/entrypoint.sh

# Создаём не-root пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Порт, который будет слушать приложение
EXPOSE 8000

# Команда запуска
CMD ["/app/docker/entrypoint.sh"]