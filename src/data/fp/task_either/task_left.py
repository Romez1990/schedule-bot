from typing import (
    Any,
    TypeVar,
)

from data.fp.either import Left
from data.fp.task_either import TaskEither

L = TypeVar('L')
R = Any


def TaskLeft(value: L) -> TaskEither[L, R]:
    return TaskEither.from_either(Left(value))
