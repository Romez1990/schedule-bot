from typing import (
    Awaitable,
    Callable,
    TypeVar,
    ParamSpec,
)

from .task import Task

P = ParamSpec('P')
T = TypeVar('T')


def taskify(fn: Callable[P, Awaitable[T]]) -> Callable[P, Task[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Task[T]:
        return Task(fn(*args, **kwargs))  # type: ignore

    return wrapper
