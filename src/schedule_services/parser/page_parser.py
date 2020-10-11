from src.http_client import AsyncHttpClient
from .page_parser_interface import PageParserInterface
from .document_factory import DocumentFactory
from .document import Document


class PageParser(PageParserInterface):
    def __init__(self, http_client: AsyncHttpClient, document_factory: DocumentFactory) -> None:
        self.__http = http_client
        self.__document_factory = document_factory

    async def parse(self, url: str) -> Document:
        html = await self.__http.html(url)
        return self.__document_factory.create(html)
