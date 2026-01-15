class Book:
    def __init__(self, title: str, author: str, price: float, id: int = None):
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if not author.strip():
            raise ValueError("Author cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")

        self.id = id  # Добавляем ID для работы с БД
        self.title = title
        self.author = author
        self.price = price

    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def update_title(self, new_title: str):
        if not new_title.strip():
            raise ValueError("Title cannot be empty")
        self.title = new_title

    def update_author(self, new_author: str):
        if not new_author.strip():
            raise ValueError("Author cannot be empty")
        self.author = new_author

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}', author='{self.author}', price={self.price})"