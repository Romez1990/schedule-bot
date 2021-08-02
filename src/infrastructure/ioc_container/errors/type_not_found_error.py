class TypeNotFoundError(Exception):
    def __init__(self, class_type: type) -> None:
        super().__init__(f'the requested service "{class_type.__name__}" has not been registered')
