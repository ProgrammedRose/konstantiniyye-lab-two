from pydantic import BaseModel, Field
from datetime import datetime

# Про Пидантик и тд говорили в файле выше...

class PurchaseCreateSchema(BaseModel):
    book_id: int = Field(..., example=1)
    quantity: int = Field(..., example=2)


class PurchaseReadSchema(BaseModel):
    book_title: str
    quantity: int
    total_price: float
    date: datetime
