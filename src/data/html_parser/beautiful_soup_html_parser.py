from infrastructure.ioc_container import service
from .html_parser import HtmlParser
from .document import Document
from .beautiful_soup_document import BeautifulSoupDocument


@service
class BeautifulSoupHtmlParser(HtmlParser):
    def parse(self, html: str) -> Document:
        return BeautifulSoupDocument(html)
