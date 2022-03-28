from __future__ import annotations


class Group:
    def __init__(self, group_name: str) -> None:
        self.__group_name = group_name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Group):
            raise NotImplemented
        return self.__group_name == other.__group_name

    def __hash__(self) -> int:
        return hash(self.__group_name)

    def __repr__(self) -> str:
        return f'Group({repr(self.__group_name)})'

    def __str__(self) -> str:
        return self.__group_name
