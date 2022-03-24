from abc import ABCMeta, abstractmethod

from .base_script import ScriptBase


class Script(ScriptBase, metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> None: ...
