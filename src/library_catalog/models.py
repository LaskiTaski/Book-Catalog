from sqlalchemy import Column, Integer, String, Boolean
from src.library_catalog.database import Base


class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    pages = Column(Integer)
    available = Column(Boolean, nullable=False, default=True)
    description = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
