import contextlib
import types

import httpx
import typing_extensions

from . import user_post_list


class Client(contextlib.AbstractAsyncContextManager["Client"]):
    def __init__(self):
        self.__client = httpx.AsyncClient()

    @typing_extensions.override
    async def __aenter__(self):
        self.__client = await self.__client.__aenter__()
        return self

    @typing_extensions.override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: types.TracebackType | None = None,
    ):
        await self.__client.__aexit__(exc_type, exc_value, traceback)

    async def aclose(self):
        await self.__client.aclose()

    def user_post_list(self, uid: int) -> user_post_list.UserPostList:
        return user_post_list.UserPostList(self.__client, uid)
