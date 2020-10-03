from typing import Optional


class EnvironmentDriver:
    def read(self) -> None:
        raise NotImplementedError

    def get_str(self, key: str) -> Optional[str]:
        raise NotImplementedError
