from typing import (
    Any,
    Type,
    Iterator,
    Mapping,
)


class TypeHints(Mapping[str, Type]):
    def __init__(self, type_hints: Mapping[str, Any]) -> None:
        [self.__check_type(type) for type in type_hints.values()]
        self.__type_hints = type_hints

    def __check_type(self, parameter_type: Type) -> None:
        if not isinstance(parameter_type, type):
            raise ValueError(f'')

    def __iter__(self) -> Iterator[str]:
        return iter(self.__type_hints)

    def __getitem__(self, key: str) -> Type:
        return self.__type_hints[key]

    def __len__(self) -> int:
        return len(self.__type_hints)
