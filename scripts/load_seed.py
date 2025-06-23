#!/usr/bin/env python
"""Load initial books into the database.

Usage:
    poetry run python scripts/load_seed.py   # или python -m scripts.load_seed
"""
import json
import pathlib
import sys

from sqlalchemy.orm import Session

# ── 1. пути и конфигурация ────────────────────────────────────────────
ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURE_FILE = ROOT / "fixtures" / "books_seed.json"


sys.path.append(str(ROOT / "src"))  # «src» должен быть в PYTHONPATH
from library_catalog.database import Base, engine  # noqa: E402
from library_catalog import models  # noqa: E402


# ── 2. читаем json, создаём таблицы, загружаем данные ─────────────────
def main() -> None:
    if not FIXTURE_FILE.exists():
        print(f"Fixture file {FIXTURE_FILE} not found", file=sys.stderr)
        sys.exit(1)

    Base.metadata.create_all(bind=engine)

    with open(FIXTURE_FILE, encoding="utf-8") as f, Session(engine) as session:
        books = json.load(f)
        # пропускаем книги, которые уже есть (id уникально)
        for item in books:
            if not session.get(models.Book, item["id"]):
                session.add(models.Book(**item))
        session.commit()

    print(f"✔  Loaded {len(books)} books into DB")


if __name__ == "__main__":
    main()
