from .document import Document


class DocumentFactory:
    def create(self, html: str) -> Document:
        raise NotImplementedError
