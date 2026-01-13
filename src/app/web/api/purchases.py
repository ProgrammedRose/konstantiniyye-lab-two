from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.app.web.schemas.purchase import (
    PurchaseCreateSchema,
    PurchaseReadSchema
)
from src.app.web.dependencies import get_purchase_service
from src.app.application.services.purchase_service import PurchaseService
from src.app.application.dto.purchase_dto import PurchaseCreateDTO

router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"]
)


@router.get("", response_model=List[PurchaseReadSchema])
def get_purchases(service: PurchaseService = Depends(get_purchase_service)):
    return service.get_all_purchases()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_purchase(
    schema: PurchaseCreateSchema,
    service: PurchaseService = Depends(get_purchase_service)
):
    dto = PurchaseCreateDTO(**schema.model_dump())
    try:
        service.create_purchase(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
