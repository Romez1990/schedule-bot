from .tag import Tag


class Document:
    def select(self, selector: str) -> Tag:
        raise NotImplementedError

    def select_all(self, selector: str) -> list[Tag]:
        raise NotImplementedError
