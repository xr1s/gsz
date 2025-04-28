import typing

from ...excel import Text
from .base import BaseModel


class CaptionSentence(BaseModel):
    caption_text_id: Text
    position: typing.Literal["Center"] | None = None
    start_time: float
    end_time: float
    ease_in: float | None = None
    ease_out: float | None = None


class Caption(BaseModel):
    caption_list: list[CaptionSentence]
