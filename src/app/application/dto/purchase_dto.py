
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PurchaseCreateDTO:
    book_id: int
    quantity: int


@dataclass
class PurchaseReadDTO:
    book_title: str
    quantity: int
    total_price: float
    date: datetime
