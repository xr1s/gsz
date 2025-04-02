import typing

from .base import Model


class Dialogue(Model):
    dialogue_progress: int | None = None
    unlock_id: int | None = None
    talk_name_id: int | None = None
    dialogue_path: str
    option_path: str | None = None


class RogueNPC(Model):
    dialogue_type: typing.Literal["Event", "Story"]
    dialogue_list: list[Dialogue]
