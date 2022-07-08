from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Chat:
    id: int
