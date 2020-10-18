from typing import (
    Tuple,
)


class Color:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.__red = red
        self.__green = green
        self.__blue = blue

    @property
    def red(self) -> int:
        return self.__red

    @property
    def green(self) -> int:
        return self.__green

    @property
    def blue(self) -> int:
        return self.__blue

    def to_tuple(self) -> Tuple[int, int, int]:
        return self.__red, self.__green, self.__blue
