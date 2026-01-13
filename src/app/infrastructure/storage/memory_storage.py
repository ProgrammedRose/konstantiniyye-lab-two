
class MemoryStorage:

# Хранилище из книг и покупок (тупо списки)
    def __init__(self):
        self.books: list = []
        self.purchases: list = []

    def clear(self):
        self.books.clear()
        self.purchases.clear()
