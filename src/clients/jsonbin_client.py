import httpx
import logging

logger = logging.getLogger(__name__)


class JsonBinClient:
    def __init__(self, bin_id: str, token: str):
        self.base_url = "https://api.jsonbin.io/v3/b"
        self.headers = {"X-Master-Key": token, "Content-Type": "application/json"}
        self.bin_id = bin_id

    def get_data(self):
        try:
            url = f"{self.base_url}/{self.bin_id}/latest"
            response = httpx.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()["record"]
        except Exception as e:
            logger.error(f"Ошибка при получении данных из JsonBin: {e}")
            raise

    def update_data(self, data):
        try:
            url = f"{self.base_url}/{self.bin_id}"
            response = httpx.put(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка при обновлении данных в JsonBin: {e}")
            raise
