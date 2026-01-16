# src.app/web/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from src.app.web.schemas.auth import LoginSchema, TokenSchema
from src.app.web.dependencies import get_auth_service
from src.app.web.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/token", response_model=TokenSchema)
def login_for_access_token(schema: LoginSchema, auth_service=Depends(get_auth_service)):
    user = auth_service.authenticate_user(schema.username, schema.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
