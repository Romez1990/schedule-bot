from src.ioc_container import Module, Container
from .page_parser_interface import PageParserInterface
from .page_parser import PageParser
from .document_factory import DocumentFactory
from .beautiful_soup_document_factory import BeautifulSoupDocumentFactory


class ParserModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(PageParser).to(PageParserInterface)
        container.bind(BeautifulSoupDocumentFactory).to(DocumentFactory)
