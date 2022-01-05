from typing import (
    Awaitable,
    Callable,
    TypeVar,
)
from aiohttp import ClientSession, ClientResponse

from infrastructure.ioc_container import service
from data.fp.task_either import TaskEither
from data.fp.either import Either, Right, Left
from .http_client import HttpClient

T = TypeVar('T')


@service
class HttpClientImpl(HttpClient):
    def get_text(self, url: str) -> TaskEither[Exception, str]:
        return self.__get(url, self.__read_text)

    def __get(self, url: str, read_response: Callable[[ClientResponse], Awaitable[T]]) -> TaskEither[Exception, T]:
        return TaskEither(self.__get_async(url, read_response))

    async def __get_async(self, url: str,
                          read_response: Callable[[ClientResponse], Awaitable[T]]) -> Either[Exception, T]:
        async with ClientSession() as session:
            try:
                response = await session.get(url)
            except Exception as e:
                return Left(e)
            else:
                if response.status >= 300:
                    return Left(RuntimeError('error status'))
                text = await read_response(response)
                return Right(text)

    def __read_text(self, response: ClientResponse) -> Awaitable[str]:
        return response.text()
