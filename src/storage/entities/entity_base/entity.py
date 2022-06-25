from data.vector import List


class Entity:
    def __setattr__(self, key: str, value: object) -> None:
        if getattr(self, key, None) is not None:
            raise RuntimeError('entity is readonly')
        super().__setattr__(key, value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__.items() == other.__dict__.items()

    def __repr__(self) -> str:
        entity_name = self.__class__.__name__
        attributes = List(self.__dict__.items()) \
            .map(self.__join_attribute_name_and_value)
        attributes_with_comma = ', '.join(attributes)
        return f'{entity_name}({attributes_with_comma})'

    def __join_attribute_name_and_value(self, item: tuple[str, object]) -> str:
        name, value = item
        return f'{name}={repr(value)}'
