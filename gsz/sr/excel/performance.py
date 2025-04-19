import enum
import typing

import typing_extensions

from .base import ModelID


class BlackType(enum.Enum):
    None_ = "None"
    Full = "Full"
    NoPost = "NoPost"
    NoPre = "NoPre"
    NoPrePost = "NoPrePost"


class Performance(ModelID):
    performance_id: int
    performance_path: str
    is_skip: typing.Literal["AfterSeen", "Always"] | None = None
    change_player_type: typing.Literal["Character", "StoryLine"] | None = None
    performance_character: str | None = None
    start_black: BlackType | None = None
    end_black: BlackType | None = None
    end_with_crack: bool = False
    plane_id: int | None = None
    floor_id: int | None = None
    group_id: int | None = None
    is_intro_dialogue: bool = False

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.performance_id
