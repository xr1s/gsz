import datetime
import enum
import typing

import pydantic

from .base import Model


def duration_milli_seconds(milli: int) -> datetime.timedelta:
    return datetime.timedelta(milliseconds=milli)


class Definition(enum.Enum):
    _480P = "480P"
    _720P = "720P"
    _1080P = "1080P"
    _2K = "2K"


class Codec(enum.Enum):
    H264 = "h264"


class Resolution(Model):
    url: pydantic.HttpUrl
    definition: Definition
    height: int
    width: int
    bitrate: int
    size: int
    format: typing.Literal["MP4", ".mp4"]
    label: Definition
    codec: Codec


class Vod(Model):
    id: int
    duration: typing.Annotated[datetime.timedelta, pydantic.BeforeValidator(duration_milli_seconds)]
    cover: pydantic.HttpUrl
    resolutions: list[Resolution]
    view_num: int
    transcoding_status: typing.Literal[2]
    review_status: typing.Literal[1, 2]
    brief_intro: typing.Literal[""] | None = None
    cover_img_id: typing.Literal["0"] | None = None
