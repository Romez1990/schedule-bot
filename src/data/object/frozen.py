class Frozen:
    def __setattr__(self, key: str, value: object) -> None:
        if hasattr(self, key):
            raise RuntimeError(f'cannot assign to field {repr(key)}')
        super().__setattr__(key, value)
