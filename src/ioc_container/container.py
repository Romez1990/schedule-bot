from __future__ import annotations
from typing import (
    get_type_hints,
    Type,
    Callable,
    TypeVar,
    TYPE_CHECKING,
)

from .errors import (
    SubclassError,
    TypeAlreadyBoundError,
    TypeMatchingError,
    TypeNotFoundError,
    MissingTypeHintError,
)
from .binding_context import BindingContext
from .type_hints import TypeHints

if TYPE_CHECKING:
    from .module import Module

T = TypeVar('T')

wrapper_descriptor = type(object.__init__)


class Container:
    def __init__(self) -> None:
        self.__types: dict[Type, Type] = {}
        self.__instances: dict[Type, object] = {}

    def register_module(self, module: Type[Module]) -> None:
        module_object = module(self)
        module_object.bind()

    def bind(self, type: Type) -> BindingContext:
        return BindingContext(type, lambda base_type: self.__bind_type(type, base_type))

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
            instance = self.__instances[base_type]
            return self.__as_type(instance, base_type)
        if base_type not in self.__types:
            raise TypeNotFoundError(base_type)
        type = self.__types[base_type]
        instance = self.__instantiate_type(type)
        del self.__types[base_type]
        self.__instances[base_type] = instance
        return self.__as_type(instance, base_type)

    def __as_type(self, instance: object, type: Type[T]) -> T:
        if not isinstance(instance, type):
            raise TypeMatchingError(instance, type)
        return instance

    def __instantiate_type(self, type: Type) -> object:
        type_hints = self.__get_constructor_type_hints(type)
        parameter_type: Type[object]
        return type(**{parameter_name: self.get(parameter_type)
                       for parameter_name, parameter_type in type_hints.items()})

    def __get_constructor_type_hints(self, type_: Type) -> TypeHints:
        constructor = type_.__init__
        if self.__is_constructor_empty(constructor):
            return TypeHints({})
        type_hints = get_type_hints(constructor)
        if 'return' in type_hints:
            del type_hints['return']
        parameter_names = self.__get_function_parameters(constructor)
        if len(type_hints) != len(parameter_names):
            parameters_with_no_type_hint = [parameter_name for parameter_name in parameter_names
                                            if parameter_name not in type_hints]
            raise MissingTypeHintError(type_, parameters_with_no_type_hint)
        return TypeHints(type_hints)

    def __is_constructor_empty(self, constructor: Callable) -> bool:
        return isinstance(constructor, wrapper_descriptor)

    def __get_function_parameters(self, func: Callable) -> list[str]:
        number_of_parameters = func.__code__.co_argcount
        self_parameter = 1
        return list(func.__code__.co_varnames[self_parameter:number_of_parameters])
