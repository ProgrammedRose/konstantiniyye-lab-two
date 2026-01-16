# src.app/grpc/handlers/books_handler.py
import asyncio
from app.grpc.protos import books_pb2, books_pb2_grpc
from src.app.infrastructure.db.session import SessionLocal
from src.app.infrastructure.repositories.sqlalchemy_book_repository import SQLAlchemyBookRepository
from src.app.application.services.book_service import BookService


class BookServiceServicer(books_pb2_grpc.BookServiceServicer):
    async def ListBooks(self, request, context):
        # synchronous DB access wrapped in threadpool
        def _get():
            db = SessionLocal()
            try:
                repo = SQLAlchemyBookRepository(db)
                service = BookService(repo)
                return service.get_all_books()
            finally:
                db.close()

        books = await asyncio.get_event_loop().run_in_executor(None, _get)
        resp = books_pb2.ListBooksResponse()
        for b in books:
            resp.books.add(id=b.id, title=b.title, author=b.author, price=b.price)
        return resp

    async def CreateBook(self, request, context):
        def _create():
            db = SessionLocal()
            try:
                repo = SQLAlchemyBookRepository(db)
                service = BookService(repo)
                from src.app.application.dto.book_dto import BookCreateDTO
                dto = BookCreateDTO(title=request.title, author=request.author, price=request.price)
                return service.add_book(dto)
            finally:
                db.close()
        book_id = await asyncio.get_event_loop().run_in_executor(None, _create)
        return books_pb2.CreateBookResponse(id=book_id)

    async def UpdateBook(self, request, context):
        def _update():
            db = SessionLocal()
            try:
                repo = SQLAlchemyBookRepository(db)
                service = BookService(repo)
                from src.app.application.dto.book_dto import BookUpdateDTO
                dto = BookUpdateDTO(title=request.title, author=request.author, price=request.price)
                service.update_book(request.id, dto)
            finally:
                db.close()
        await asyncio.get_event_loop().run_in_executor(None, _update)
        return books_pb2.Empty()

    async def DeleteBook(self, request, context):
        def _delete():
            db = SessionLocal()
            try:
                repo = SQLAlchemyBookRepository(db)
                service = BookService(repo)
                service.delete_book(request.id)
            finally:
                db.close()
        await asyncio.get_event_loop().run_in_executor(None, _delete)
        return books_pb2.Empty()
