from .document import Document


class PageParserInterface:
    async def parse(self, url: str) -> Document:
        raise NotImplementedError
