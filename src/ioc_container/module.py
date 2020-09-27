from .container_builder import ContainerBuilder


class Module:
    def __init__(self, builder: ContainerBuilder) -> None:
        self.__builder = builder

    def _load(self, builder: ContainerBuilder) -> None:
        raise NotImplementedError

    def bind(self) -> None:
        self._load(self.__builder)
