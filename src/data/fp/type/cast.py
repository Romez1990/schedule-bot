from typing import (
    Callable,
    Type,
    TypeVar,
    cast as typing_cast,
)

T = TypeVar('T')


def cast(_: Type[T]) -> Callable[[object], T]:
    def mapper(value: object) -> T:
        return typing_cast(T, value)

    return mapper
