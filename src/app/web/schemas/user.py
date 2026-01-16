# src/app/web/schemas/user.py
from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    username: str = Field(..., example="alice")
    password: str = Field(..., example="secret")
    role: str | None = Field(None, example="user")  # admin may set; public registration ignores role


class UserReadSchema(BaseModel):
    id: int
    username: str
    role: str
