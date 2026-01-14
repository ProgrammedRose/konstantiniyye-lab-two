from sqlalchemy.orm import Session
from typing import List
from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.domain.entities.purchase import Purchase
from src.app.application.dto.purchase_dto import PurchaseCreateDTO
from src.app.infrastructure.db.models.purchase_model import PurchaseModel
from src.app.infrastructure.db.models.book_model import BookModel
from datetime import datetime

# Репозиторий покупок
class SQLAlchemyPurchaseRepository(PurchaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Purchase]:
        purchases = self.db.query(PurchaseModel).all()
        result = []
        for p in purchases:
            book = p.book
            result.append(
                Purchase(
                    book=book,
                    quantity=p.quantity,
                    total_price=float(p.total_price),
                    date=p.date
                )
            )
        return result

    def add(self, dto: PurchaseCreateDTO, book_price: float) -> int:
        total_price = dto.quantity * book_price
        purchase = PurchaseModel(
            book_id=dto.book_id,
            quantity=dto.quantity,
            total_price=total_price,
            date=datetime.utcnow()
        )
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase.id
