class SubclassError(Exception):
    def __init__(self, class_type: type, base_class: type) -> None:
        super().__init__(f'type "{class_type.__name__}" is not subclass of "{base_class.__name__}"')
