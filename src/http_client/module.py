from src.ioc_container import Module, Container
from .async_http_client import AsyncHttpClient
from .aio_http_client import AioHttpClient


class HttpModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(AioHttpClient).to(AsyncHttpClient)
