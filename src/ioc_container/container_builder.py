from __future__ import annotations
from typing import (
    get_type_hints,
    Type,
    Callable,
    Dict,
    TYPE_CHECKING,
)
from returns.maybe import Maybe, Some, Nothing

from .binding_builder import BindingBuilder
from .container import Container

if TYPE_CHECKING:
    from .module import Module


class ContainerBuilder:
    def __init__(self) -> None:
        self.__types: Dict[Type, Type] = {}
        self.__objects: Dict[Type, object] = {}

    def bind(self, type: Type) -> BindingBuilder:
        return BindingBuilder(type, self.__create_binding_callback(type))

    def __create_binding_callback(self, type: Type) -> Callable[[Type], None]:
        return lambda base_type: self.__bind_type(type, base_type)

    def __bind_type(self, type: Type, base_type: Type) -> None:
        if not issubclass(type, base_type):
            raise Exception()
        if base_type in self.__types:
            raise Exception('type already registered')
        self.__types[base_type] = type

    def register_module(self, module: Type[Module]) -> None:
        module_object = module(self)
        module_object.bind()

    def build(self) -> Container:
        while self.__types:
            new_types = {**self.__types}
            for base_type, type in self.__types.items():
                maybe_object = self.__try_instantiate_type(type)
                if maybe_object != Nothing:
                    del new_types[base_type]
                    self.__objects[base_type] = maybe_object.unwrap()
            self.__types = new_types
        return Container(self.__objects)

    def __try_instantiate_type(self, type: Type) -> Maybe[object]:
        type_hints = get_type_hints(type.__init__)
        if 'return' in type_hints:
            del type_hints['return']
        required_parameters: Dict[str, object] = {}
        for parameter_name, parameter_type in type_hints.items():
            if parameter_type not in self.__objects:
                if parameter_type not in self.__types:
                    raise Exception(f'type {parameter_type.__name__} not bound')
                return Nothing
            required_parameters[parameter_name] = self.__objects[parameter_type]
        return Some(type(**required_parameters))
