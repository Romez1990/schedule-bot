from os import getenv
from dotenv import load_dotenv

from infrastructure.ioc_container import service
from .env_reader import EnvReader


@service
class EnvReaderImpl(EnvReader):
    def __init__(self) -> None:
        load_dotenv()

    def get_str(self, var_name: str) -> str | None:
        return getenv(var_name)
