# src.app/grpc/handlers/purchases_handler.py
import asyncio
from app.grpc.protos import purchases_pb2_grpc, purchases_pb2
from src.app.infrastructure.db.session import SessionLocal
from src.app.infrastructure.repositories.sqlalchemy_purchase_repository import SQLAlchemyPurchaseRepository
from src.app.infrastructure.repositories.sqlalchemy_book_repository import SQLAlchemyBookRepository
from src.app.application.services.purchase_service import PurchaseService


class PurchaseServiceServicer(purchases_pb2_grpc.PurchaseServiceServicer):
    async def ListPurchases(self, request, context):
        def _get():
            db = SessionLocal()
            try:
                p_repo = SQLAlchemyPurchaseRepository(db)
                b_repo = SQLAlchemyBookRepository(db)
                service = PurchaseService(p_repo, b_repo)
                return service.get_all_purchases()
            finally:
                db.close()

        purchases = await asyncio.get_event_loop().run_in_executor(None, _get)
        resp = purchases_pb2.ListPurchasesResponse()
        for p in purchases:
            resp.purchases.add(book_title=p.book_title, quantity=p.quantity, total_price=p.total_price, date=p.date.isoformat())
        return resp

    async def CreatePurchase(self, request, context):
        def _create():
            db = SessionLocal()
            try:
                p_repo = SQLAlchemyPurchaseRepository(db)
                b_repo = SQLAlchemyBookRepository(db)
                service = PurchaseService(p_repo, b_repo)
                from src.app.application.dto.purchase_dto import PurchaseCreateDTO
                dto = PurchaseCreateDTO(book_id=request.book_id, quantity=request.quantity)
                service.create_purchase(dto)
                return True
            finally:
                db.close()
        success = await asyncio.get_event_loop().run_in_executor(None, _create)
        return purchases_pb2.CreatePurchaseResponse(success=success)
