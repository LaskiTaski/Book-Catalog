import abc
import httpx
import logging

logger = logging.getLogger(__name__)


class BaseApiClient(abc.ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    @abc.abstractmethod
    async def fetch(self, *args, **kwargs):
        pass

    async def _get(self, url: str, params: dict = None):
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка при GET-запросе к {url}: {e}")
            raise

    async def __aexit__(self, *args):
        await self.client.aclose()
