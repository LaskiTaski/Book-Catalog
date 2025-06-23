import json
import os

BOOKS_FILE = "books.json"


def load_books_from_file():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_books_to_file(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def get_next_id(books):
    return max([book["id"] for book in books], default=0) + 1
