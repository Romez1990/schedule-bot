from abc import ABCMeta

from infrastructure.ioc_container import Container


class ScriptBase(metaclass=ABCMeta):
    container: Container
