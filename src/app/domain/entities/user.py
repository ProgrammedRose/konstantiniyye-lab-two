# src/app/domain/entities/user.py
class User:
    def __init__(self, username: str, password_hash: str, role: str = "user", id: int = None):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not password_hash:
            raise ValueError("Password hash cannot be empty")
        if role not in ("admin", "user"):
            # anonymous не хранится в БД, роль для записываемых пользователей — admin или user
            raise ValueError("Role must be 'admin' or 'user'")
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', role='{self.role}')"
