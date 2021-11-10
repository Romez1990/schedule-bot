from infrastructure.ioc_container import service
from .http_client import HttpClient


@service
class HttpClientImpl(HttpClient):
    def html(self, url: str) -> str:
        return 'lasdjfal'
