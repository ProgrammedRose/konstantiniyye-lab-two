from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

# API routers
from src.app.web.api.books import router as books_api_router
from src.app.web.api.purchases import router as purchases_api_router

# dependencies
from src.app.web.dependencies import get_book_service, get_purchase_service

# application services
from src.app.application.services.book_service import BookService
from src.app.application.services.purchase_service import PurchaseService

# DTO
from src.app.application.dto.purchase_dto import PurchaseCreateDTO



# Делаем FastAPI app
app = FastAPI(
    title="Bookstore Application",
    description="Lab 01 - WEB Techs",
    version="1.0.1"
)



# API (JSON и Swagger)
app.include_router(books_api_router)
app.include_router(purchases_api_router)



# Шаблон HTML...
# Тут используем минимальный юай адаптер Фаста к Jinja2
# Он шаблонизирует наш HTML и дает нам готовую HTML-страницу

templates = Jinja2Templates(directory="src/app/web/views")

# HTML Веб страницы
@app.get("/web/books", response_class=HTMLResponse)
def web_books(
    request: Request,
    service: BookService = Depends(get_book_service)
):
    books = service.get_all_books()
    return templates.TemplateResponse(
        "books.html",
        {"request": request, "books": books}
    )


@app.get("/web/purchase", response_class=HTMLResponse)
def web_purchase_form(
    request: Request,
    service: BookService = Depends(get_book_service)
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
    service: PurchaseService = Depends(get_purchase_service)
):
    purchases = service.get_all_purchases()
    return templates.TemplateResponse(
        "purchases.html",
        {"request": request, "purchases": purchases}
    )


# Root redirect
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(
        url="/web/books",
        status_code=HTTP_303_SEE_OTHER
    )
