from aiohttp import ClientSession, ClientResponse

from infrastructure.ioc_container import service
from data.fp.task_either import TaskEither
from data.fp.either import Either, Right, Left
from .http_client import HttpClient


@service
class HttpClientImpl(HttpClient):
    def html(self, url: str) -> TaskEither[Exception, str]:
        return self.__get(url) \
            .bind_awaitable(self.__get_text_async)

    async def __get_text_async(self, response: ClientResponse) -> str:
        return await response.text()

    def __get(self, url: str) -> TaskEither[Exception, ClientResponse]:
        return TaskEither(self.__get_async(url))

    async def __get_async(self, url: str) -> Either[Exception, ClientResponse]:
        async with ClientSession() as session:
            try:
                response = await session.get(url)
            except Exception as e:
                return Left(e)
            else:
                if response.status >= 300:
                    return Left(RuntimeError('error status'))
                return Right(response)
