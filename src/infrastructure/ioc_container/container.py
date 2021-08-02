from collections.abc import (
    Sequence,
    Mapping,
    MutableMapping,
)
from typing import (
    Optional,
    Type,
    Callable,
    TypeVar,
    get_type_hints,
    cast,
)
from types import (
    WrapperDescriptorType,
)

from data.vector import (
    Dict,
)
from .errors import (
    SubclassError,
    TypeAlreadyBoundError,
    TypeNotFoundError,
    MissingTypeHintError,
    WrongTypeHintError,
    UselessAdditionalParametersError,
)
from .binding_context import BindingContext
from .module import Module

T = TypeVar('T')


class Container:
    def __init__(self) -> None:
        self.__types: MutableMapping[type, type] = {}
        self.__instances: MutableMapping[type, object] = {}

    def register_module(self, module: Type[Module]) -> None:
        module_object = module(self)
        module_object.load()

    def bind(self, class_type: type) -> BindingContext:
        def bind_to_base_class(base_class: Optional[type], to_self: bool) -> None:
            self.__bind_type(class_type, base_class, to_self)

        return BindingContext(bind_to_base_class)

    def __bind_type(self, class_type: type, base_class_optional: Optional[type], to_self: bool) -> None:
        base_class = cast(type, base_class_optional) if not to_self else class_type
        if not issubclass(class_type, base_class):
            raise SubclassError(class_type, base_class)
        if base_class in self.__types:
            class_type = self.__types[base_class]
            raise TypeAlreadyBoundError(base_class, class_type)
        elif base_class in self.__instances:
            instance = self.__instances[base_class]
            raise TypeAlreadyBoundError(base_class, type(instance))
        self.__types[base_class] = class_type

    def get(self, base_class: Type[T]) -> T:
        if base_class in self.__instances:
            instance = self.__instances[base_class]
            return cast(T, instance)
        if base_class not in self.__types:
            raise TypeNotFoundError(base_class)
        class_type = self.__types[base_class]
        instance = self.__instantiate_type(class_type)
        del self.__types[base_class]
        self.__instances[base_class] = instance
        return instance

    def create(self, class_type: Type[T], additional_parameters: Mapping[str, object] = None) -> T:
        return self.__instantiate_type(class_type, additional_parameters)

    def __instantiate_type(self, class_type: type,
                           additional_parameters_optional: Mapping[str, object] = None) -> T:
        additional_parameters: Mapping[str, object] = \
            additional_parameters_optional if additional_parameters_optional is not None else {}
        type_hints = self.__get_constructor_type_hints(class_type)
        required_parameters = self.__subtract_additional_parameters(class_type, type_hints, additional_parameters)
        parameter_instances = Dict(required_parameters).map(self.__cast_type).map(self.get)
        instance = class_type(**parameter_instances, **additional_parameters)
        return cast(T, instance)

    def __get_constructor_type_hints(self, class_type: type) -> Mapping[str, type]:
        constructor = class_type.__init__  # type: ignore
        if self.__is_constructor_empty(constructor):
            return {}
        type_hints = get_type_hints(constructor)
        if 'return' in type_hints:
            del type_hints['return']
        parameter_names = self.__get_function_parameters(constructor)
        if len(type_hints) != len(parameter_names):
            parameters_with_no_type_hint = [parameter_name for parameter_name in parameter_names
                                            if parameter_name not in type_hints]
            raise MissingTypeHintError(class_type, parameters_with_no_type_hint)
        return {name: self.__check_type_hint(name, parameter_type) for name, parameter_type in type_hints.items()}

    def __is_constructor_empty(self, constructor: Callable) -> bool:
        return isinstance(constructor, WrapperDescriptorType)

    def __get_function_parameters(self, func: Callable) -> Sequence[str]:
        number_of_parameters = func.__code__.co_argcount
        self_parameter = 1
        return list(func.__code__.co_varnames[self_parameter:number_of_parameters])

    def __check_type_hint(self, name: str, parameter_type: object) -> type:
        if not isinstance(parameter_type, type):
            raise WrongTypeHintError(name, parameter_type)
        return parameter_type

    def __subtract_additional_parameters(self, class_type: type, type_hints: Mapping[str, type],
                                         additional_parameters: Mapping[str, object]) -> Mapping[str, type]:
        additional_parameters_set = set(additional_parameters.keys())
        new_type_hints = {}
        for parameter_name in type_hints:
            if parameter_name not in additional_parameters_set:
                new_type_hints[parameter_name] = type_hints[parameter_name]
            else:
                additional_parameters_set.remove(parameter_name)
        if len(additional_parameters_set) > 0:
            raise UselessAdditionalParametersError(class_type, additional_parameters_set)
        return new_type_hints

    def __cast_type(self, type_value: type) -> Type[object]:
        return cast(Type[object], type_value)
