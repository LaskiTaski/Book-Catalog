from fastapi import FastAPI, HTTPException
from typing import List, Optional
from .models import Book, BookCreate

app = FastAPI()

# "База данных" в памяти
books_db = []
next_id = 1


@app.get("books/", response_model=List[Book])
def get_books(author: Optional[str] = None,
              genre: Optional[str] = None,
              available: Optional[str] = None) -> List[Book]:
    result = books_db
    if author:
        result = [book for book in result if book["author"].lower() == author.lower()]
    if genre:
        result = [book for book in result if book["genre"].lower() == genre.lower()]
    if available:
        result = [book for book in result if book["available"].lower() == available.lower()]

    return result


@app.get("books/{book_id}", response_model=Book)
def get_book(book_id: int) -> Book:
    for book in books_db:
        if book['id'] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.post("books/", response_model=Book)
def add_book(book: BookCreate) -> None:
    global next_id
    book_dict = book.model_dump()
    book_dict["id"] = next_id
    next_id += 1
    books_db.append(book_dict)
    return book_dict


@app.put("books/{book_id}", response_model=Book)
def add_book(book_id: int, updated_book: BookCreate) -> Book:
    for book in books_db:
        if book['id'] == book_id:
            book.update(updated_book.model_dump())
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.delete("books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Книга не найдена")
