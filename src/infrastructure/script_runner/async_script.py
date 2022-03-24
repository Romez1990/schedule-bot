from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .base_script import ScriptBase


class AsyncScript(ScriptBase, metaclass=ABCMeta):
    @abstractmethod
    def run(self) -> Awaitable[None]: ...
