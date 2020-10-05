from .document_factory import DocumentFactory
from .document import Document
from .beautiful_soup_document import BeautifulSoupDocument


class BeautifulSoupDocumentFactory(DocumentFactory):
    def create(self, html: str) -> Document:
        return BeautifulSoupDocument(html)
