from typing import (
    TypeVar,
    Callable,
)

T = TypeVar('T')


def const(value: T) -> Callable[[], T]:
    return lambda: value
