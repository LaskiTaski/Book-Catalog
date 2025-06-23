import os
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.library_catalog import models, schemas, database
from src.library_catalog.repository import BookRepository

from src.clients.openlibrary_client import OpenLibraryClient
from src.clients.jsonbin_client import JsonBinClient

models.Base.metadata.create_all(bind=database.engine)

JSONBIN_TOKEN = os.getenv("JSONBIN_TOKEN")
JSONBIN_BIN_ID = os.getenv("JSONBIN_BIN_ID")
# Инициализация клиентов
jsonbin_client = JsonBinClient(bin_id=JSONBIN_BIN_ID, token=JSONBIN_TOKEN)

openlibrary_client = OpenLibraryClient()

app = FastAPI(
    title="Library Catalog API",
    description="API для управления каталогом книг",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)


# Dependense
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/books/", response_model=List[schemas.Book])
async def get_books(
    author: Optional[str] = None,
    genre: Optional[str] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    repo = BookRepository(db)
    return repo.get_all(author=author, genre=genre, available=available)


@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.post("/books/", response_model=schemas.Book)
async def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    repo = BookRepository(db)

    # Попробуем найти данные в OpenLibrary
    enriched = await openlibrary_client.get_data(book.title)
    if enriched:
        if not book.author and enriched["author"]:
            book.author = enriched["author"]
        if not book.description and enriched["description"]:
            book.description = str(enriched["description"])
        if not book.cover_url and enriched["cover_id"]:
            book.cover_url = openlibrary_client.get_cover_url(enriched["cover_id"])

    return repo.create(book)


@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(get_db)
):
    repo = BookRepository(db)
    book = repo.update(book_id, updated_book)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    book = repo.delete(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"ok": True, "msg": "Success"}
