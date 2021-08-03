from typing import (
    TypeVar,
)

T = TypeVar('T')


async def async_identity(value: T) -> T:
    return value
