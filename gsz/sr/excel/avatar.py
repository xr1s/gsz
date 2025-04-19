import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import item
from .base import Element, ModelID, Path, Text, Value


class Rarity(enum.Enum):
    Type4 = "CombatPowerAvatarRarityType4"
    Type5 = "CombatPowerAvatarRarityType5"


class AvatarConfig(ModelID):
    avatar_id: int
    avatar_name: Text
    avatar_full_name: Text
    adventure_player_id: int
    avatar_vo_tag: typing.Annotated[str, pydantic.Field(alias="AvatarVOTag")]
    rarity: Rarity
    json_path: pathlib.Path
    damage_type: Element
    sp_need: Value[int] | None = None  # 遐蝶 SP 是 None
    exp_group: typing.Literal[1]
    max_promotion: typing.Literal[6]
    max_rank: typing.Literal[6]
    rank_id_list: list[int]
    reward_list: list[item.Pair]
    skill_list: list[int]
    avatar_base_type: Path
    default_avatar_model_path: str
    default_avatar_head_icon_path: str
    avatar_side_icon_path: str
    avatar_mini_icon_path: str
    avatar_gacha_result_img_path: str
    action_avatar_head_icon_path: str
    ultra_skill_cut_in_prefab_path: str
    ui_avatar_model_path: str
    manikin_json_path: str
    ai_path: str
    skilltree_prefab_path: str
    damage_type_resistance: list[None]
    release: bool
    side_avatar_head_icon_path: str
    waiting_avatar_head_icon_path: str
    avatar_cutin_img_path: str
    avatar_cutin_bg_img_path: typing.Annotated[str, pydantic.Field(alias="AvatarCutinBgImgPath")]
    avatar_cutin_front_img_path: str
    avatar_cutin_intro_text: Text | None = None
    avatar_drop_offset: list[float]
    avatar_trial_offset: list[float]
    player_card_offset: list[float]
    assist_offset: list[float]
    assist_bg_offset: typing.Annotated[list[float], pydantic.Field(alias="AssistBgOffset")]
    avatar_self_show_offset: list[float]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.avatar_id
