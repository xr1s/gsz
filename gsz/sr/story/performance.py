import enum
import typing

import pydantic

from .base import Model


class Type(enum.Enum):
    A = "A"
    C = "C"
    D = "D"
    E = "E"
    PlayVideo = "PlayVideo"


class CreateCharacter(Model):
    character_unique_name: str
    avatar_id: str
    area_name: str
    anchor_name: str | None = None


class EntityVisiable(Model):
    group_id: int
    group_npc_id: int


class PropVisiable(Model):
    group_id: int
    prop_id: int


class CaptureNPC(Model):
    character_unique_name: str | None
    group_id: int | None
    npc_id: typing.Annotated[int, pydantic.Field(alias="NpcID")]


class FindType(enum.Enum):
    ByOther = "ByOther"


class CaptureTeam(Model):
    unique_name: str
    character_id: int | None = None
    find_type: FindType | None = None
