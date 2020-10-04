from os import getenv
from typing import (
    Optional,
)
from dotenv import load_dotenv

from .environment_driver import EnvironmentDriver


class DotEnvEnvironmentDriver(EnvironmentDriver):
    def read(self) -> None:
        load_dotenv()

    def get_str(self, key: str) -> Optional[str]:
        return getenv(key)
