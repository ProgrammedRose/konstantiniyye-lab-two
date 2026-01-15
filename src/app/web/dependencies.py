from fastapi import Depends

from src.app.infrastructure.db.session import get_db
from src.app.infrastructure.repositories.sqlalchemy_book_repository import SQLAlchemyBookRepository
from src.app.infrastructure.repositories.sqlalchemy_purchase_repository import SQLAlchemyPurchaseRepository
from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService
from sqlalchemy.orm import Session

def get_book_repository(db: Session = Depends(get_db)):
    return SQLAlchemyBookRepository(db)

def get_purchase_repository(db: Session = Depends(get_db)):
    return SQLAlchemyPurchaseRepository(db)

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    repository = get_book_repository(db)
    return BookService(repository)

def get_purchase_service(db: Session = Depends(get_db)) -> PurchaseService:
    book_repository = get_book_repository(db)
    purchase_repository = get_purchase_repository(db)
    return PurchaseService(purchase_repository, book_repository)