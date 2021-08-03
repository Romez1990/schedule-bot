from typing import (
    TypeVar,
)

from data.fp.maybe import Some
from data.fp.task_maybe import TaskMaybe

T = TypeVar('T')


def TaskSome(value: T) -> TaskMaybe[T]:
    return TaskMaybe.from_maybe(Some(value))
