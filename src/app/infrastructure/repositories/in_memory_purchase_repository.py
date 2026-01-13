# app/infrastructure/repositories/in_memory_purchase_repository.py
from typing import List
from src.app.application.ports.purchase_repository import PurchaseRepository
from src.app.domain.entities.purchase import Purchase
from src.app.infrastructure.storage.memory_storage import MemoryStorage


class InMemoryPurchaseRepository(PurchaseRepository):

    def __init__(self, storage: MemoryStorage):
        self.storage = storage

    def get_all(self) -> List[Purchase]:
        return self.storage.purchases.copy()

    def add(self, purchase: Purchase) -> None:
        self.storage.purchases.append(purchase)

    def count(self) -> int:
        return len(self.storage.purchases)
