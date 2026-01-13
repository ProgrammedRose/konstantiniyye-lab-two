
from dataclasses import dataclass

# Эти dataclass автоматически генерят иниты и repr (аналог toString)
# Плюс это как защита от логики внутри классов, в этих классах нам нужны только данные.
# ДТО нужно, чтобы передавать данные между слоями.

# А вот почему не использовать пидантик и тут? Очевидно, чтобы не позволять разным слоям
# склеиваться (пидантик используется Фаст Апи), ведь пидантик есть веб слой.... вот потому и датакласс

@dataclass
class BookCreateDTO:
    title: str
    author: str
    price: float


@dataclass
class BookUpdateDTO:
    title: str
    author: str
    price: float


@dataclass
class BookReadDTO:
    id: int
    title: str
    author: str
    price: float
