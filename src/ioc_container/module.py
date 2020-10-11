from .container import Container


class Module:
    def __init__(self, container: Container) -> None:
        self.__container = container

    def _load(self, container: Container) -> None:
        raise NotImplementedError

    def bind(self) -> None:
        self._load(self.__container)
