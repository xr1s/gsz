import collections.abc
import datetime

import httpx
import typing_extensions

from . import exception, model

API = "https://bbs-api.miyoushe.com/painter/wapi/userPostList"


class StructuredContent:
    def __init__(self, structured_content: model.StructuredContent):
        self.__structured_content = structured_content

    def is_(self, sc: type):
        return isinstance(self.__structured_content.insert, sc)

    @property
    def bold(self) -> bool:
        return self.__structured_content.attributes.bold if self.__structured_content.attributes is not None else False

    @property
    def italic(self) -> bool:
        return (
            self.__structured_content.attributes.italic if self.__structured_content.attributes is not None else False
        )

    @property
    def text(self) -> str | None:
        return self.__structured_content.insert if isinstance(self.__structured_content.insert, str) else None

    @property
    def image(self) -> str | None:
        if not isinstance(self.__structured_content.insert, model.structured_content.Image):
            return None
        if self.__structured_content.insert.image == "true":
            return None
        return str(self.__structured_content.insert.image)

    @property
    def video(self) -> str | None:
        if isinstance(self.__structured_content.insert, model.structured_content.Video):
            return str(self.__structured_content.insert.video)
        if isinstance(self.__structured_content.insert, model.structured_content.Vod):
            if len(self.__structured_content.insert.vod.resolutions) == 0:
                return None
            resolution = max(
                self.__structured_content.insert.vod.resolutions,
                key=lambda resolution: resolution.width * resolution.height,
            )
            return str(resolution.url)
        return None

    @property
    def video_cover(self) -> str | None:
        if not isinstance(self.__structured_content.insert, model.structured_content.Vod):
            return None
        return str(self.__structured_content.insert.vod.cover)


class Post:
    def __init__(self, post: model.UserPost):
        self.__post = post

    @property
    def id(self) -> int:
        return self.__post.post.post_id

    @property
    def subject(self) -> str:
        return self.__post.post.subject

    @property
    def created_at(self) -> datetime.datetime:
        return self.__post.post.created_at.astimezone()

    def structured_content(self) -> collections.abc.Iterable[StructuredContent]:
        return (
            ()
            if self.__post.post.structured_content is None
            else (StructuredContent(structured_content) for structured_content in self.__post.post.structured_content)
        )


class UserPost(collections.abc.AsyncIterator[Post]):
    def __init__(self, client: httpx.AsyncClient, uid: int):
        self.__client = client
        self.__uid = uid
        # size=50 是后端限制的单次请求上限
        self.__params: dict[str, int] = {"size": 50, "uid": uid}
        self.__user_posts: list[model.user_post.UserPost] = []
        self.__iter_index: int = 0
        self.__is_last: bool = False

    @typing_extensions.override
    def __aiter__(self) -> typing_extensions.Self:
        return self

    @typing_extensions.override
    async def __anext__(self) -> Post:
        if self.__iter_index == len(self.__user_posts) and self.__is_last:
            raise StopAsyncIteration
        if self.__iter_index != len(self.__user_posts):
            self.__iter_index += 1
            return Post(self.__user_posts[self.__iter_index - 1])
        res = await self.__client.get(API, params=self.__params)
        res = res.raise_for_status()
        res = model.Response[model.user_post.UserPostList].model_validate_json(res.content)
        if res.retcode != 0:
            raise exception.APIException(API, self.__params, res.retcode, res.message)
        if len(res.data.list) == 0:
            raise StopAsyncIteration
        self.__user_posts = res.data.list
        self.__iter_index = 1
        self.__params["offset"] = res.data.next_offset
        self.__is_last = res.data.is_last
        return Post(self.__user_posts[0])


class UserPostList(collections.abc.AsyncIterable[Post]):
    def __init__(self, client: httpx.AsyncClient, uid: int):
        self.__client = client
        self.__uid = uid

    @typing_extensions.override
    def __aiter__(self) -> UserPost:
        return UserPost(self.__client, self.__uid)
