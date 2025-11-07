import enum
import typing

import pydantic
import typing_extensions

from .base import ModelID, Text


class BillboardType(enum.Enum):
    _ = "None"
    Icon = "Icon"
    Sneak = "Sneak"


class SpecialType(enum.Enum):
    _ = "NPC_SPECIAL_NONE"
    Aranara = "NPC_SPECIAL_ARANARA"
    PlayerBoy = "NPC_SPECIAL_PLAYER_BOY"
    PlayerGirl = "NPC_SPECIAL_PLAYER_GIRL"


class Npc(ModelID):
    action_id_list: tuple[int, ...]
    alias: str
    animator_config_path_hash: Text
    avatar_id: typing.Annotated[int, pydantic.Field(alias="avatarID")]
    billboard_icon: str
    billboard_type: BillboardType
    body_type: str
    camp_id: typing.Annotated[int, pydantic.Field(alias="campID")]
    controller_path_hash: typing.Literal[0]
    controller_path_remote_hash: typing.Literal[0]
    deformation_mesh_path_hash: int
    disable_show_name: bool
    element_type: typing.Literal["None"]
    feature_tag_group_id: int
    first_met_id: int
    has_audio: bool
    has_move: bool
    id_: int
    invisiable: bool
    is_daily: bool
    json_name: str
    json_path_hash: int
    lod_pattern_name: typing.Literal[""]
    lua_data_index: int
    lua_data_path: str
    name_text_map_hash: int
    prefab_path_hash: int
    prefab_path_remote_hash: typing.Literal[0]
    script_data_path: str
    special_type: SpecialType
    template_emotion_path: str
    unique_body_id: int
    # unknown: typing.Annotated[bool, pydantic.Field(alias="CJLOKMBHLKF")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="IFKPLLOEOFC")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="IPILCCDOKDL")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="JECEIBLKBLF")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="JGAECHAMOPA")]
    # unknown: typing.Annotated[typing.Literal[''], pydantic.Field(alias="LLIIMGOOMOP")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="MHEMMGAGGDK")]
    # unknown: typing.Annotated[bool, pydantic.Field(alias="PHLLCAOKLIB")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
