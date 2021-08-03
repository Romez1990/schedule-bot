from os import getenv
from typing import (
    Optional,
)
from dotenv import load_dotenv

from infrastructure.ioc_container import service
from .env_reader import EnvReader


@service
class EnvReaderImpl(EnvReader):
    def __init__(self) -> None:
        load_dotenv()

    def get_str(self, var_name: str) -> Optional[str]:
        return getenv(var_name)
