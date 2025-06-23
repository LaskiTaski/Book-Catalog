from .base_client import BaseApiClient


class OpenLibraryClient(BaseApiClient):
    BASE_URL = "https://openlibrary.org"

    def __init__(self) -> None:
        super().__init__(self.BASE_URL)

    async def fetch(self, title: str):
        return await self.get_data(title)

    async def get_data(self, title: str):
        params = {"title": title}
        result = await self._get("/search.json", params=params)
        if not result or "docs" not in result or not result["docs"]:
            return None

        doc = result["docs"][0]
        return {
            "title": doc.get("title"),
            "author": doc.get("author_name", [None])[0],
            "cover_id": doc.get("cover_i"),
            "description": doc.get("first_sentence") or doc.get("subtitle"),
            "rating": doc.get("ratings_average"),  # может не быть
        }

    def get_cover_url(self, cover_id: int) -> str:
        return (
            f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else ""
        )
