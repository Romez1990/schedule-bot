from typing import (
    Any,
    TypeVar,
)

from data.fp.either import Right
from data.fp.task_either import TaskEither

L = Any
R = TypeVar('R')


def TaskRight(value: R) -> TaskEither[L, R]:
    return TaskEither.from_either(Right(value))
