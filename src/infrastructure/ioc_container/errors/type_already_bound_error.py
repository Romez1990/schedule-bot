class TypeAlreadyBoundError(Exception):
    def __init__(self, base_class: type, class_type: type) -> None:
        super().__init__(f'type "{base_class.__name__}" is already bound to "{class_type.__name__}"')
