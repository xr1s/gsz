import datetime
import typing

import pydantic

from .base import Model

D = typing.TypeVar("D")


class Response(Model, typing.Generic[D]):
    code: int
    message: str
    ttl: typing.Literal[1] | None = None
    data: D


class Nav(Model):
    class WbiImg(Model):
        img_url: pydantic.HttpUrl
        sub_url: pydantic.HttpUrl

    is_login: typing.Annotated[bool, pydantic.Field(alias="isLogin")]
    wbi_img: WbiImg


class FingerSpi(Model):
    b_3: str
    b_4: str


class VideoMetaState(Model):
    season_id: int
    view: int
    danmaku: int
    reply: int
    favorite: int
    coin: int
    share: int
    like: int
    mtime: datetime.datetime
    vt: typing.Literal[0]
    vv: typing.Literal[0]


class VideoMeta(Model):
    id: int
    title: str
    cover: pydantic.HttpUrl
    mid: int
    intro: str
    sign_state: typing.Literal[0]
    attribute: int
    stat: VideoMetaState
    ep_count: int
    first_aid: int
    ptime: datetime.datetime
    ep_num: int


class Video(Model):
    comment: int
    typeid: int
    play: int
    pic: pydantic.HttpUrl
    subtitle: str
    description: str
    copyright: typing.Literal["1"]
    title: str
    review: typing.Literal[0]
    author: str
    mid: int
    created: datetime.datetime
    length: datetime.timedelta
    video_review: int
    aid: int
    bvid: str
    hide_click: bool
    is_pay: typing.Literal[0]
    is_union_video: typing.Literal[0, 1]
    is_steins_gate: typing.Literal[0]
    is_live_playback: typing.Literal[0]
    is_lesson_video: typing.Literal[0]
    is_lesson_finished: typing.Literal[0]
    lesson_update_info: str
    jump_url: str
    meta: VideoMeta | None
    is_avoided: typing.Literal[0]
    season_id: int
    attribute: int
    is_charging_arc: bool
    elec_arc_type: typing.Literal[0]
    elec_arc_badge: typing.Literal[""]
    vt: typing.Literal[0]
    enable_vt: typing.Literal[0]
    vt_display: typing.Literal[""]
    playback_position: typing.Literal[0]
    is_self_view: bool

    @pydantic.field_validator("length", mode="before")
    @classmethod
    def length_to_timedelta(cls, value: str) -> datetime.timedelta:
        minutes, seconds = value.split(":")
        return datetime.timedelta(minutes=int(minutes), seconds=int(seconds))


class Search(Model):
    class T(Model):
        tid: int
        count: int
        name: str

    class List(Model):
        slist: list[None] | None = None
        tlist: dict[int, "Search.T"] | None = None
        vlist: list[Video]

    class Page(Model):
        pn: int
        ps: int
        count: int

    class EpisodicButton(Model):
        text: str
        uri: str  # 相对路径 "//www.bilibili.com/media..." 形式

    class GaiaData(Model):
        pass

    list: List
    page: Page
    episodic_button: EpisodicButton | None = None
    is_risk: bool
    gaia_res_type: typing.Literal[0]
    gaia_data: None
