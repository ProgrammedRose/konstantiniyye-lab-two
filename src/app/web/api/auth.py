from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.web.schemas.auth import (
    UserCreateSchema,
    UserLoginSchema,
    TokenSchema,
    UserReadSchema
)
from src.app.web.dependencies import get_db, get_auth_service
from src.app.application.services.auth_service import AuthService
from src.app.application.dto.auth_dto import UserCreateDTO, UserLoginDTO

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserCreateSchema,
        auth_service: AuthService = Depends(get_auth_service)
):
    """Регистрация нового пользователя"""
    try:
        dto = UserCreateDTO(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )

        user = await auth_service.register_user(dto)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenSchema)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Аутентификация пользователя и получение JWT токена"""
    dto = UserLoginDTO(
        username=form_data.username,
        password=form_data.password
    )

    token = await auth_service.authenticate_user(dto)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


@router.get("/me", response_model=UserReadSchema)
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service)
):
    """Получить информацию о текущем пользователе"""
    user = await auth_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserReadSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )