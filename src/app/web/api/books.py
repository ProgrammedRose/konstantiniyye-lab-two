from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from fastapi.security import OAuth2PasswordBearer

from src.app.web.schemas.book import (
    BookCreateSchema,
    BookUpdateSchema,
    BookReadSchema
)
from src.app.web.dependencies import get_book_service
from src.app.application.services.book_service import BookService
from src.app.application.dto.book_dto import BookCreateDTO, BookUpdateDTO

router = APIRouter(
    prefix="/api/books",
    tags=["Books"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("", response_model=List[BookReadSchema])
async def get_books(service: BookService = Depends(get_book_service)):
    """Получить все книги (публичный доступ)"""
    return await service.get_all_books()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
    schema: BookCreateSchema,
    token: str = Depends(oauth2_scheme),  # Требуется аутентификация
    service: BookService = Depends(get_book_service)
):
    """Создать новую книгу (требуется аутентификация)"""
    dto = BookCreateDTO(**schema.model_dump())
    book_id = await service.add_book(dto)
    return {"id": book_id}


@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
    book_id: int,
    schema: BookUpdateSchema,
    token: str = Depends(oauth2_scheme),  # Требуется аутентификация
    service: BookService = Depends(get_book_service)
):
    """Обновить книгу (требуется аутентификация)"""
    dto = BookUpdateDTO(**schema.model_dump())
    try:
        await service.update_book(book_id, dto)
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    token: str = Depends(oauth2_scheme),  # Требуется аутентификация
    service: BookService = Depends(get_book_service)
):
    """Удалить книгу (требуется аутентификация)"""
    try:
        await service.delete_book(book_id)
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail="Book not found")