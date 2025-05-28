import collections.abc
import contextlib
import datetime
import hashlib
import itertools
import pathlib
import time
import types
import typing
import urllib.parse

import fake_useragent
import httpx
import typing_extensions

from . import exception, model

MIXIN_KEY_ENC_TAB: bytes = (
    b"./\x12\x025\x08\x17 \x0f2\n\x1f:\x03-#\x1b+\x051!\t*\x13\x1d\x1c\x0e'\x0c&)\r"
    b'%0\x07\x10\x187(=\x1a\x11\x00\x01<3\x1e\x04\x16\x196\x158;\x06?9>\x0b$\x14",4'
)


class Client(contextlib.AbstractAsyncContextManager["Client"]):
    def __init__(self):
        self.__client = httpx.AsyncClient(
            headers={"user-agent": fake_useragent.UserAgent(os=["Windows"]).random},
            event_hooks={"request": [self.sign]},
        )
        self.__wbi_key = b""
        self.__wbi_key_date = datetime.datetime.now().astimezone().date()
        self.__mixin_key: bytes = b""

    @typing_extensions.override
    async def __aenter__(self):
        self.__client = await self.__client.__aenter__()
        await self.set_buvid()
        self.__mixin_key = await self.mixin_key()
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

    async def wbi_key(self) -> bytes:
        if self.__wbi_key != b"" and datetime.datetime.now().astimezone().date() == self.__wbi_key_date:
            return self.__wbi_key
        res = await self.__client.get("https://api.bilibili.com/x/web-interface/nav")
        _ = res.raise_for_status()
        nav = model.bilibili.Response[model.bilibili.Nav].model_validate_json(res.content)
        img = pathlib.PurePosixPath(nav.data.wbi_img.img_url.path or "").stem
        sub = pathlib.PurePosixPath(nav.data.wbi_img.sub_url.path or "").stem
        self.__wbi_key = (img + sub).encode()
        self.__wbi_key_date = datetime.datetime.now().astimezone().date()
        return self.__wbi_key

    async def mixin_key(self) -> bytes:
        wbi_key = await self.wbi_key()
        return bytes(wbi_key[k] for k in MIXIN_KEY_ENC_TAB[:32])

    SIGNATURE: list[tuple[str, str]] = [
        ("dm_img_str", "bm8gd2ViZ2"),
        ("dm_cover_img_str", "bm8gd2ViZ2"),
        ("dm_img_list", "[]"),
        ("dm_img_inter", '{"wh":[0,0,0],"of":[0,0,0]}'),
    ]

    async def sign(self, request: httpx.Request):
        params = itertools.chain(request.url.params.items(), self.SIGNATURE, [("wts", str(round(time.time())))])
        params = {key: "".join(char for char in val if char not in "!'()*") for key, val in sorted(params)}
        query = urllib.parse.urlencode(params).replace("+", "%20").encode()
        params["w_rid"] = hashlib.md5(query + self.__mixin_key).hexdigest()
        request.url = request.url.copy_with(params=params)

    async def set_buvid(self):
        # 初始化一些 set-cookie
        res = await self.__client.get("https://api.bilibili.com/x/frontend/finger/spi")
        _ = res.raise_for_status()
        res = model.bilibili.Response[model.bilibili.FingerSpi].model_validate_json(res.content)
        self.__client.cookies.set("buvid3", res.data.b_3)
        self.__client.cookies.set("buvid4", res.data.b_4, domain=".bilibili.com", path="/")

    def space(self, mid: int) -> "Space":
        return Space(self.__client, mid)


class Space:
    def __init__(self, client: httpx.AsyncClient, mid: int):
        self.__client = client
        self.__mid = mid

    def search(self, keyword: str = "") -> "SearchIterable":
        """查询投稿视频"""
        return SearchIterable(self.__client, self.__mid, keyword)


class Video:
    def __init__(self, video: model.bilibili.Video):
        self.__video = video

    @property
    def title(self) -> str:
        return self.__video.title

    @property
    def bvid(self) -> str:
        return self.__video.bvid

    @property
    def cover(self) -> str:
        return str(self.__video.pic)

    @property
    def is_union_video(self) -> bool:
        return self.__video.is_union_video == 1


class SearchIterable(collections.abc.AsyncIterable[Video]):
    def __init__(self, client: httpx.AsyncClient, mid: int, keyword: str):
        self.__client = client
        self.__mid = mid
        self.__keyword = keyword

    @typing_extensions.override
    def __aiter__(self) -> "SearchIterator":
        return SearchIterator(self.__client, self.__mid, self.__keyword)


class SearchIterator(collections.abc.AsyncIterator[Video]):
    API: str = "https://api.bilibili.com/x/space/wbi/arc/search"

    def __init__(self, client: httpx.AsyncClient, mid: int, keyword: str):
        class Params(typing.TypedDict):
            pn: int  # 页码
            ps: int  # 单页返回视频数量，后端限制的单次请求上限 50
            mid: int  # 用户 ID
            keyword: str  # 搜索内容，留空为列出全部

        self.__client = client
        self.__params = Params(pn=0, ps=50, mid=mid, keyword=keyword)
        self.__videos: list[model.bilibili.Video] = []
        self.__iter_index: int = 0
        self.__count: int | None = None

    @typing_extensions.override
    def __aiter__(self) -> typing_extensions.Self:
        return self

    @typing_extensions.override
    async def __anext__(self) -> Video:
        if (
            self.__iter_index == len(self.__videos)
            and self.__count is not None
            and self.__params["pn"] * self.__params["ps"] >= self.__count
        ):
            raise StopAsyncIteration
        if self.__iter_index != len(self.__videos):
            self.__iter_index += 1
            return Video(self.__videos[self.__iter_index - 1])
        self.__params["pn"] += 1
        res = await self.__client.get(
            self.API,
            headers={"referer": f"https://space.bilibili.com/{self.__params['mid']}/upload/video"},
            params=typing.cast(collections.abc.Mapping[str, int | str], self.__params),
        )
        res = res.raise_for_status()
        res = model.bilibili.Response[model.bilibili.Search].model_validate_json(res.content)
        if res.code != 0:
            raise exception.APIException(self.API, self.__params, res.code, res.message)
        self.__videos = res.data.list.vlist
        self.__count = res.data.page.count
        self.__iter_index = 0
        return Video(self.__videos[0])
