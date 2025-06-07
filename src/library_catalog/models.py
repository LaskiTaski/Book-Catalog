from pydantic import BaseModel
from typing import Optional


# Основной класс основанный на BaseModel
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    genre: str
    pages: int
    available: bool


# Класс для создания книг основанный на BookBase
class BookCreate(BookBase):
    pass


# Класс для получения книги с возможностью фильтрации основанный на BookBase
class Book(BookBase):
    id: int

    class Config:
        from_attributes = True  # Нужно для совместимости с БД в будущем
