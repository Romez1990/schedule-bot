from typing import Optional


class AbstractBaseEnvironment:
    def read(self) -> None:
        raise NotImplementedError

    def get_str(self, key: str) -> Optional[str]:
        raise NotImplementedError
