from src.ioc_container import Module, ContainerBuilder
from .page_parser_interface import PageParserInterface
from .page_parser import PageParser
from .document_factory import DocumentFactory
from .beautiful_soup_document_factory import BeautifulSoupDocumentFactory


class ParserModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(PageParser).to(PageParserInterface)
        builder.bind(BeautifulSoupDocumentFactory).to(DocumentFactory)
