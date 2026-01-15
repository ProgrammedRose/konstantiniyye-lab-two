from typing import Optional

from pydantic import BaseModel, Field

# Пидантик нужен нам в связи со Сваггером (в рамках Фаст АПИ):
# Фаст читает BaseModel, строит схемы и уже на их основе делает нам Swagger UI (короче - от
# описания структуры до визуализации).

# Собственно, почему и был выбран Фаст АПИ, а не частично знакомый мне Фласк, - это по той
# причине, что с Фастом есть автоматическая генерация документации :))))

    # В общем, как это работает:
    #   FastAPI анализирует код (читает там методы, пути и так далее) и
    #       делает OpenAPI-спецификацию (JSON-документ)
    #   Swagger UI отображает OpenAPI

# Что есть BaseModel? Фактически, он (пидантик) гарантирует нам, что поля в
# классах ниже будут иметь заданные именно мной типы (это вроде как называется контрактом).

# Еще этот пидантик парсит джесон, проверяет типы, ну и выбрасывает ошибки, если что-то не так.

# Зачем Field()? Ну, он был в примере, мной использованном, и как я понял, может задавать
# допограничения и примеры.

class BookCreateSchema(BaseModel):
    title: str = Field(..., example="Clean Architecture")
    author: str = Field(..., example="Robert C. Martin")
    price: float = Field(..., example=39.99)


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None


class BookReadSchema(BaseModel):
    id: int
    title: str
    author: str
    price: float
