class DecoratingClassNameError(Exception):
    def __init__(self, class_type: type, suffix: str) -> None:
        super().__init__(f'decorating object name "{class_type.__name__}" must ends with "{suffix}"')
