from typing import (
    TypeVar,
)

from data.fp.maybe import Nothing
from data.fp.task_maybe import TaskMaybe

T = TypeVar('T')


def TaskNothing() -> TaskMaybe[T]:
    return TaskMaybe.from_maybe(Nothing)
