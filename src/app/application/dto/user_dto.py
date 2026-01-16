# src/app/application/dto/user_dto.py
from dataclasses import dataclass


@dataclass
class UserCreateDTO:
    username: str
    password: str
    role: str | None = None  # optional: admin can set, registration won't set admin


@dataclass
class UserReadDTO:
    id: int
    username: str
    role: str
