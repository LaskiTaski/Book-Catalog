from sqlalchemy.orm import Session
from . import models, schemas


class BookRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, author=None, genre=None, available=None):
        query = self.db.query(models.Book)
        if author:
            query = query.filter(models.Book.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
        if available is not None:
            query = query.filter(models.Book.available == available)
        return query.all()

    def get_by_id(self, book_id: int):
        return self.db.query(models.Book).filter(models.Book.id == book_id).first()

    def create(self, book_data: schemas.BookCreate):
        new_book = models.Book(**book_data.dict())
        self.db.add(new_book)
        self.db.commit()
        self.db.refresh(new_book)
        return new_book

    def update(self, book_id: int, updated_data: schemas.BookCreate):
        book = self.get_by_id(book_id)
        if book:
            for key, value in updated_data.model_dump(exclude_unset=True).items():
                setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
        return book

    def delete(self, book_id: int):
        book = self.get_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
        return book
