from __future__ import annotations
from typing import (
    get_type_hints,
    Type,
    List,
    Dict,
    Callable,
    TypeVar,
    TYPE_CHECKING,
)

from .errors import (
    SubclassError,
    TypeAlreadyBoundError,
    TypeNotFoundError,
    MissingTypeHintError,
)
from .binding_builder import BindingBuilder
from .type_hints import TypeHints

if TYPE_CHECKING:
    from .module import Module

T = TypeVar('T')

wrapper_descriptor = type(object.__init__)


class Container:
    def __init__(self) -> None:
        self.__types: Dict[Type, Type] = {}
        self.__instances: Dict[Type, object] = {}

    def register_module(self, module: Type[Module]) -> None:
        module_object = module(self)
        module_object.bind()

    def bind(self, type: Type) -> BindingBuilder:
        return BindingBuilder(type, lambda base_type: self.__bind_type(type, base_type))

    def __bind_type(self, type: Type, base_type: Type) -> None:
        if not issubclass(type, base_type):
            raise SubclassError(type, base_type)
        if base_type in self.__types:
            type = self.__types[base_type]
            raise TypeAlreadyBoundError(base_type, type)
        elif base_type in self.__instances:
            instance = self.__instances[base_type]
            raise TypeAlreadyBoundError(base_type, type(instance))
        self.__types[base_type] = type

    def get(self, base_type: Type[T]) -> T:
        if base_type in self.__instances:
            return self.__instances[base_type]
        if base_type not in self.__types:
            raise TypeNotFoundError(base_type)
        type = self.__types[base_type]
        instance = self.__instantiate_type(type)
        del self.__types[base_type]
        self.__instances[base_type] = instance
        return instance

    def __instantiate_type(self, type: Type) -> object:
        type_hints = self.__get_constructor_type_hints(type)
        return type(**{parameter_name: self.get(parameter_type)
                       for parameter_name, parameter_type in type_hints.items()})

    def __get_constructor_type_hints(self, type_: Type) -> TypeHints:
        constructor = type_.__init__
        if self.__is_constructor_empty(constructor):
            return TypeHints({})
        type_hints = get_type_hints(constructor)
        if 'return' in type_hints:
            del type_hints['return']
        parameter_names: List[str] = [parameter_name for parameter_name in constructor.__code__.co_varnames
                                      if parameter_name != 'self']
        if len(type_hints) != len(parameter_names):
            parameters_with_no_type_hint = [parameter_name for parameter_name in parameter_names
                                            if parameter_name not in type_hints]
            raise MissingTypeHintError(type_, parameters_with_no_type_hint)
        return TypeHints(type_hints)

    def __is_constructor_empty(self, constructor: Callable) -> bool:
        return type(constructor) == wrapper_descriptor
