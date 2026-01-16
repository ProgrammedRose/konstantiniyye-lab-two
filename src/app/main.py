# src.app/main.py
import os
import asyncio
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_303_SEE_OTHER
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# API routers
from src.app.web.api.books import router as books_api_router
from src.app.web.api.purchases import router as purchases_api_router
from src.app.web.api.auth import router as auth_api_router
from src.app.web.api.users import router as users_api_router

# dependencies
from src.app.web.dependencies import get_book_service, get_purchase_service, get_db
from src.app.web.security import get_current_user

# application services
from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService

# DTO
from src.app.application.dto.purchase_dto import PurchaseCreateDTO

# DB initialization
from src.app.infrastructure.db.base import Base
from src.app.infrastructure.db.session import engine, SessionLocal
from src.app.infrastructure.db.models import BookDB, PurchaseDB  # noqa: F401

# grpc
from src.app.grpc.server import serve as start_grpc_server
import asyncio

load_dotenv()

# Create tables if not exists
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bookstore Application",
    description="Lab 02 -> Lab 03 - WEB + Roles + gRPC",
    version="3.0.0"
)

# Include API routers without global auth dependency; endpoints themselves have role deps
app.include_router(books_api_router)
app.include_router(purchases_api_router)
app.include_router(auth_api_router)
app.include_router(users_api_router)

templates = Jinja2Templates(directory="src/app/web/views")


@app.on_event("startup")
async def startup_event():
    # start grpc server in background as a task
    loop = asyncio.get_event_loop()
    loop.create_task(start_grpc_server())


@app.get("/web/books", response_class=HTMLResponse)
def web_books(
    request: Request,
    service: BookService = Depends(get_book_service),
    db: Session = Depends(get_db)
):
    books = service.get_all_books()
    return templates.TemplateResponse(
        "books.html",
        {"request": request, "books": books}
    )

@app.get("/web/purchase", response_class=HTMLResponse)
def web_purchase_form(
    request: Request,
    service: BookService = Depends(get_book_service),
    db: Session = Depends(get_db)
):
    books = service.get_all_books()
    return templates.TemplateResponse(
        "purchase.html",
        {"request": request, "books": books}
    )

@app.post("/web/purchase")
def web_create_purchase(
    book_id: int = Form(...),
    quantity: int = Form(...),
    purchase_service: PurchaseService = Depends(get_purchase_service)
):
    dto = PurchaseCreateDTO(book_id=book_id, quantity=quantity)

    try:
        purchase_service.create_purchase(dto)
    except ValueError as e:
        return HTMLResponse(
            f"<h3>Error: {e}</h3><a href='/web/purchase'>Back</a>",
            status_code=400
        )

    return RedirectResponse(
        url="/web/purchases",
        status_code=HTTP_303_SEE_OTHER
    )

@app.get("/web/purchases", response_class=HTMLResponse)
def web_purchases(
    request: Request,
    service: PurchaseService = Depends(get_purchase_service),
    db: Session = Depends(get_db)
):
    purchases = service.get_all_purchases()
    return templates.TemplateResponse(
        "purchases.html",
        {"request": request, "purchases": purchases}
    )

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(
        url="/web/books",
        status_code=HTTP_303_SEE_OTHER
    )
