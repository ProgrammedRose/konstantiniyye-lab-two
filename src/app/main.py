from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_303_SEE_OTHER

# API routers
from src.app.web.api.books import router as books_api_router
from src.app.web.api.purchases import router as purchases_api_router
from src.app.web.api.auth import router as auth_api_router  # НОВЫЙ

# dependencies
from src.app.web.dependencies import get_book_service, get_purchase_service, get_auth_service

# application services
from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService
from src.app.application.services.auth_service import AuthService

# DTO
from src.app.application.dto.purchase_dto import PurchaseCreateDTO

# Создаём FastAPI app
app = FastAPI(
    title="Bookstore Application",
    description="Lab 02 - WEB Techs with PostgreSQL & Authentication",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Регистрируем API роутеры
app.include_router(books_api_router)
app.include_router(purchases_api_router)
app.include_router(auth_api_router)  # НОВЫЙ

# Настраиваем Jinja2 шаблоны
templates = Jinja2Templates(directory="src/app/web/views")

# OAuth2 для веб-страниц
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# HTML Веб страницы
@app.get("/web/books", response_class=HTMLResponse)
async def web_books(
    request: Request,
    service: BookService = Depends(get_book_service)
):
    books = await service.get_all_books()
    return templates.TemplateResponse(
        "books.html",
        {"request": request, "books": books}
    )


@app.get("/web/purchase", response_class=HTMLResponse)
async def web_purchase_form(
    request: Request,
    service: BookService = Depends(get_book_service)
):
    books = await service.get_all_books()
    return templates.TemplateResponse(
        "purchase.html",
        {"request": request, "books": books}
    )


@app.post("/web/purchase")
async def web_create_purchase(
    book_id: int = Form(...),
    quantity: int = Form(...),
    purchase_service: PurchaseService = Depends(get_purchase_service)
):
    dto = PurchaseCreateDTO(book_id=book_id, quantity=quantity)

    try:
        await purchase_service.create_purchase(dto)
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
async def web_purchases(
    request: Request,
    service: PurchaseService = Depends(get_purchase_service)
):
    purchases = await service.get_all_purchases()
    return templates.TemplateResponse(
        "purchases.html",
        {"request": request, "purchases": purchases}
    )


# НОВЫЕ: Страницы аутентификации
@app.get("/web/login", response_class=HTMLResponse)
async def web_login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@app.get("/web/register", response_class=HTMLResponse)
async def web_register_form(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


# Root redirect
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(
        url="/web/books",
        status_code=HTTP_303_SEE_OTHER
    )


# Health check для Docker
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy", "service": "bookstore-api"}


# События запуска/остановки приложения
@app.on_event("startup")
async def startup_event():
    print("Application starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutting down...")