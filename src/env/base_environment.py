from os import getenv
from typing import Optional
from dotenv import load_dotenv

from .abstract_base_environment import AbstractBaseEnvironment


class BaseEnvironment(AbstractBaseEnvironment):
    def read(self) -> None:
        load_dotenv()

    def get_str(self, key: str) -> Optional[str]:
        return getenv(key)
