# src.app/web/api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.app.web.schemas.user import UserCreateSchema, UserReadSchema
from src.app.application.dto.user_dto import UserCreateDTO
from src.app.web.dependencies import get_user_service, get_user_service_admin
from src.app.application.services.user_service import UserService
from src.app.web.security import get_current_user, require_role

router = APIRouter(prefix="/api/users", tags=["Users"])


# Public registration: creates user with role 'user' regardless of provided role
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(schema: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    dto = UserCreateDTO(username=schema.username, password=schema.password, role=schema.role)
    user_id = user_service.create_user(dto, allow_role_setting=False)
    return {"id": user_id}


# Admin endpoints (list, create with role, delete)
@router.get("", response_model=List[UserReadSchema], dependencies=[Depends(require_role(["admin"]))])
def list_users(user_service: UserService = Depends(get_user_service_admin)):
    return user_service.get_all_users()


@router.post("/admin", response_model=dict, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(["admin"]))])
def create_user_admin(schema: UserCreateSchema, user_service: UserService = Depends(get_user_service_admin)):
    dto = UserCreateDTO(username=schema.username, password=schema.password, role=schema.role)
    user_id = user_service.create_user(dto, allow_role_setting=True)
    return {"id": user_id}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(["admin"]))])
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service_admin)):
    try:
        user_service.delete_user(user_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
