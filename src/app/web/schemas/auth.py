# src/app/web/schemas/auth.py
from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
