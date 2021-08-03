from typing import (
    Awaitable,
    Callable,
    TypeVar,
)

from .task import Task

T = TypeVar('T')


def taskify(fn: Callable[[...], Awaitable[T]]) -> Callable[[...], Task[T]]:  # type: ignore
    def wrapper(*args: object, **kwargs: object) -> Task[T]:
        return Task(fn(*args, **kwargs))  # type: ignore

    return wrapper
