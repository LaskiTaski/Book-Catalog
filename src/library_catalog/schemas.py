from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    available: bool = True
    description: Optional[str] = None
    cover_url: Optional[str] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    available: Optional[bool] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
