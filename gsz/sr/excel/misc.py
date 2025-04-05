import collections.abc
import datetime
import enum
import typing

import pydantic
import typing_extensions

from .base import ModelID, ModelMainSubID, Text, Value


class ExtraEffectConfig(ModelID):
    """效果说明。游戏界面中文字上一般会有【】配合下划线装饰，点击会弹出全屏遮罩，遮罩上是名词的详细介绍"""

    extra_effect_id: int
    extra_effect_name: Text
    extra_effect_desc: Text
    desc_param_list: list[Value[float]]
    extra_effect_icon_path: str
    extra_effect_type: typing.Literal[1, 2, 3]  # 目前只有 1, 2, 3，从对应的描述上看 1 3 都是开发用数据，不露出

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.extra_effect_id


class RewardData(ModelID):
    reward_id: int
    hcoin: int | None = None
    item_id: list[int | None] | None = None
    count: list[int | None] | None = None
    level: list[typing.Literal[1] | None] | None = None
    rank: list[typing.Literal[1] | None] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.reward_id

    @pydantic.model_validator(mode="before")
    @classmethod
    def model_validator(cls, data: typing.Any) -> typing.Any:
        class RewardData(typing.TypedDict, total=False):
            RewardID: int
            Hcoin: int | None
            ItemID: collections.abc.Sequence[int | None] | None
            Count: collections.abc.Sequence[int | None] | None
            Level: collections.abc.Sequence[int | None] | None
            Rank: collections.abc.Sequence[int | None] | None

        def field(
            returns: RewardData,
            name: typing.Literal["ItemID", "Count", "Level", "Rank"],
            pos: list[tuple[int, int]],
        ):
            if len(pos) == 0:
                return
            items: list[int | None] = [None] * max(pos)[0]
            for index, item in pos:
                items[index - 1] = item
            returns[name] = items

        if not isinstance(data, dict):
            raise TypeError(f"RewardData must be dict, {data}")
        data = typing.cast(dict[str, int], data)
        item_id_pos: list[tuple[int, int]] | None = []
        count_pos: list[tuple[int, int]] | None = []
        level_pos: list[tuple[int, int]] | None = []
        rank_pos: list[tuple[int, int]] | None = []
        reward_data: RewardData = {}
        for key, val in data.items():
            if key in ("RewardID", "Hcoin"):
                reward_data[key] = val
            elif key.startswith("ItemID_"):
                item_id_pos.append((int(key[7:]), val))
            elif key.startswith("Count_"):
                count_pos.append((int(key[6:]), val))
            elif key.startswith("Level_"):
                level_pos.append((int(key[6:]), val))
            elif key.startswith("Rank_"):
                rank_pos.append((int(key[5:]), val))
        field(reward_data, "ItemID", item_id_pos)
        field(reward_data, "Count", count_pos)
        field(reward_data, "Level", level_pos)
        field(reward_data, "Rank", rank_pos)
        return reward_data

    @pydantic.model_serializer
    def model_serializer(self) -> dict[str, int]:
        def field(returns: dict[str, int], key: str, val: int | None):
            if val is not None:
                returns[key] = val

        reward_data: dict[str, int] = {
            "RewardID": self.reward_id,
        }
        field(reward_data, "Hcoin", self.hcoin)
        name_fields: tuple[tuple[str, collections.abc.Sequence[int | None] | None], ...] = (
            ("ItemID", self.item_id),
            ("Count", self.count),
            ("Rank", self.rank),
            ("Level", self.level),
        )
        for name, fields in name_fields:
            if fields is None:
                continue
            for index, val in enumerate(fields):
                field(reward_data, f"{name}_{index + 1}", val)
        return reward_data


class MazeBuffType(enum.Enum):
    Assistant = "Assistant"
    Character = "Character"
    CharacterKeepScene = "CharacterKeepScene"
    Level = "Level"
    LevelKeepScene = "LevelKeepScene"
    Team = "Team"
    TeamKeepScene = "TeamKeepScene"


class InBattleBindingType(enum.Enum):
    CharacterAbility = "CharacterAbility"
    CharacterSkill = "CharacterSkill"
    StageAbilityAfterCharacterBorn = "StageAbilityAfterCharacterBorn"
    StageAbilityBeforeCharacterBorn = "StageAbilityBeforeCharacterBorn"


class MazeBuffUseType(enum.Enum):
    AddBattleBuff = "AddBattleBuff"
    Special = "Special"
    SummonUnit = "SummonUnit"
    TriggerBattle = "TriggerBattle"


class MazeBuffIcon(enum.Enum):
    Buff = "Buff"
    Debuff = "Debuff"
    Other = "Other"


class MazeBuff(ModelMainSubID):
    """战斗增益（或减益）。各种模拟宇宙祝福、逐光捡金效果都会链接到这里"""

    id_: int
    buff_series: typing.Literal[1]
    buff_rarity: typing.Literal[1]
    lv: int
    lv_max: int
    modifier_name: str
    in_battle_binding_type: InBattleBindingType | None = None
    in_battle_binding_key: str
    param_list: list[Value[float]]
    buff_desc_param_by_avatar_skill_id: int | None = None
    buff_icon: str
    buff_name: Text
    buff_desc: Text
    buff_simple_desc: Text | None = None
    buff_desc_battle: Text | None = None
    buff_effect: str
    maze_buff_type: MazeBuffType
    use_type: MazeBuffUseType | None = None  # 仅出现在 1.6 及之前
    maze_buff_icon_type: MazeBuffIcon | None = None
    maze_buff_pool: int | None = None
    is_display: bool = False
    is_display_env_in_level: bool = False

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.id_

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.lv


class ScheduleData(ModelID):
    id_: int
    begin_time: datetime.datetime
    end_time: datetime.datetime

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class TextJoinType(enum.Enum):
    AvatarID = "AvatarID"
    CustomText = "CustomText"


class TextJoinConfig(ModelID):
    text_join_id: int
    default_item: int
    text_join_item_list: list[int]
    is_override: bool = False
    type: TextJoinType | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.text_join_id


class TextJoinItem(ModelID):
    text_join_item_id: int
    text_join_text: Text | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.text_join_item_id
