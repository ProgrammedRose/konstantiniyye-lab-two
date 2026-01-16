# src.app/web/api/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.app.web.schemas.book import (
    BookCreateSchema,
    BookUpdateSchema,
    BookReadSchema
)
from src.app.web.dependencies import get_book_service
from src.app.application.services.book_service import BookService
from src.app.application.dto.book_dto import BookCreateDTO, BookUpdateDTO
from src.app.web.security import require_role

router = APIRouter(
    prefix="/api/books",
    tags=["Books"]
)


@router.get("", response_model=List[BookReadSchema])
def get_books(service: BookService = Depends(get_book_service)):
    return service.get_all_books()


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(["admin"]))])
def create_book(
    schema: BookCreateSchema,
    service: BookService = Depends(get_book_service)
):
    dto = BookCreateDTO(**schema.model_dump())
    book_id = service.add_book(dto)
    return {"id": book_id}


@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["admin"]))])
def update_book(
    book_id: int,
    schema: BookUpdateSchema,
    service: BookService = Depends(get_book_service)
):
    dto = BookUpdateDTO(**schema.model_dump())
    try:
        service.update_book(book_id, dto)
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["admin"]))])
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    try:
        service.delete_book(book_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="Book not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
