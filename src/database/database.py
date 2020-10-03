from typing import (
    Any,
    List,
    Dict,
)
from returns.maybe import Maybe


class Database:
    async def connect(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    async def execute(self, query: str, *args: Any) -> None:
        raise NotImplementedError

    async def fetch(self, query: str, *args: Any) -> List[Dict[str, Any]]:
        raise NotImplementedError

    async def fetch_row(self, query: str, *args: Any) -> Maybe[Dict[str, Any]]:
        raise NotImplementedError

    async def fetch_value(self, query: str, *args: Any) -> Any:
        raise NotImplementedError
