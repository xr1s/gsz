import enum
import pathlib
import typing

import typing_extensions

from .base import ModelID, ModelStringID


class CutSceneConfig(ModelStringID):
    cut_scene_name: str
    is_player_involved: bool = False
    cut_scene_path: str
    cut_scene_sfx_json_path: typing.Literal[""]
    sfx_id: int | None = None
    voice_id: int | None = None
    cut_scene_bgm_state_name: str
    caption_path: str
    pos_off_set: list[float]
    maze_plane_id: int | None = None
    maze_floor_id: int | None = None
    hide_block_list: list[typing.Literal["SquareBlock"]]

    @property
    @typing_extensions.override
    def id(self) -> str:
        return self.cut_scene_name


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


class VideoConfig(ModelID):
    video_id: int
    video_path: str
    is_player_involved: bool = False
    caption_path: str
    encryption: typing.Literal[True]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.video_id
