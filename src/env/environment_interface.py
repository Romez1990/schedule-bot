class EnvironmentInterface:
    def read(self) -> None:
        raise NotImplementedError

    def get_str(self, key: str) -> str:
        raise NotImplementedError

    def get_bool(self, key: str) -> bool:
        raise NotImplementedError

    def get_int(self, key: str) -> int:
        raise NotImplementedError

    def get_float(self, key: str) -> float:
        raise NotImplementedError
