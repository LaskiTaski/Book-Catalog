from fastapi import FastAPI, HTTPException
from typing import List, Optional
from .models import Book, BookCreate
from .storage import load_books_from_file, save_books_to_file, get_next_id

app = FastAPI()


@app.get("/books/", response_model=List[Book])
def get_books(author: Optional[str] = None,
              genre: Optional[str] = None,
              available: Optional[bool] = None) -> List[Book]:

    books_db = load_books_from_file()
    result = books_db
    if author:
        result = [book for book in result if book["author"].lower() == author.lower()]
    if genre:
        result = [book for book in result if book["genre"].lower() == genre.lower()]
    if available is not None:
        result = [book for book in result if book["available"] == available]
    return result


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> Book:
    books_db = load_books_from_file()
    for book in books_db:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.post("/books/", response_model=Book)
def add_book(book: BookCreate) -> Book:
    books_db = load_books_from_file()
    book_dict = book.model_dump()
    book_dict["id"] = get_next_id(books_db)
    books_db.append(book_dict)
    save_books_to_file(books_db)
    return book_dict


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookCreate) -> Book:
    books_db = load_books_from_file()
    for book in books_db:
        if book['id'] == book_id:
            book.update(updated_book.model_dump())
            save_books_to_file(books_db)
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    books_db = load_books_from_file()
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[i]
            save_books_to_file(books_db)
            return {
                "ok": True,
                'msg': 'Success'
            }
    raise HTTPException(status_code=404, detail="Книга не найдена")
