from aiohttp import ClientSession

from .async_http_client import AsyncHttpClient


class AioHttpClient(AsyncHttpClient):
    async def html(self, url: str) -> str:
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
