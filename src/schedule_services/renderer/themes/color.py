from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Color:
    red: int
    green: int
    blue: int

    def to_tuple(self) -> tuple[int, int, int]:
        return self.red, self.green, self.blue
