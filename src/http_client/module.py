from src.ioc_container import Module, ContainerBuilder
from .async_http_client import AsyncHttpClient
from .aio_http_client import AioHttpClient


class HttpModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(AioHttpClient).to(AsyncHttpClient)
