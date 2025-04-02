import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import aliases
from .base import Model, ModelID, ModelMainSubID, Text, Value


class Path(enum.Enum):
    """模拟、差分宇宙命途"""

    Preservation = "Preservation"
    """存护"""
    Remembrance = "Remembrance"
    """记忆"""
    Nihility = "Nihility"
    """虚无"""
    Abundance = "Abundance"
    """丰饶"""
    TheHunt = "TheHunt"
    """巡猎"""
    Destruction = "Destruction"
    """毁灭"""
    Elation = "Elation"
    """欢愉"""
    Propagation = "Propagation"
    """繁育"""
    Erudition = "Erudition"
    """智识"""
    Harmony = "Harmony"
    """同谐"""


class RogueBonus(ModelID):
    """进入宇宙的时候获取祝福的名称"""

    bonus_id: int
    bonus_event: int
    bonus_title: Text
    bonus_desc: Text
    bonus_tag: Text
    bonus_icon: typing.Literal["SpriteOutput/AvatarProfessionTattoo/Profession/BgPathsExplore.png"]  # 全是开拓祝福

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.bonus_id


class BuffCategory(enum.Enum):
    Common = "Common"
    """一星祝福"""
    Rare = "Rare"
    """二星祝福"""
    Legendary = "Legendary"
    """三星祝福"""

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case self.Common:
                return "1星"
            case self.Rare:
                return "2星"
            case self.Legendary:
                return "3星"


class BattleEventBuffType(enum.Enum):
    BattleEventBuff = "BattleEventBuff"
    BattleEventBuffCross = "BattleEventBuffCross"
    BattleEventBuffEnhance = "BattleEventBuffEnhance"


class AeonID(enum.Enum):  # 因为是回想、构音和交错，所以没有同谐
    Preservation = 1
    """存护"""
    Remembrance = 2
    """记忆"""
    Nihility = 3
    """虚无"""
    Abundance = 4
    """丰饶"""
    TheHunt = 5
    """巡猎"""
    Destruction = 6
    """毁灭"""
    Elation = 7
    """欢愉"""
    Propagation = 8
    """繁育"""
    Erudition = 9
    """智识"""


class RogueBuff(ModelMainSubID):
    """模拟宇宙祝福"""

    maze_buff_id: int
    maze_buff_level: int
    rogue_buff_type: int
    rogue_buff_rarity: typing.Literal[1, 2, 3, 4] | None = None
    # 祝福稀有度，仅出现在 2.2 及之前，2.3 被 RogueBuffCategory 取代
    rogue_buff_category: BuffCategory | None = None
    rogue_buff_tag: int
    extra_effect_id_list: list[int]
    aeon_id: AeonID | None = None
    rogue_version: typing.Literal[1]
    unlock_id_list: list[int]
    is_show: bool = False
    battle_event_buff_type: BattleEventBuffType | None = None
    activity_module_id: int | None = None  #  仅出现在 1.3 及之后
    handbook_unlock_desc: Text | None = None
    aeon_cross_icon: str | None = None  #  仅出现在 1.3 及之后，寰宇蝗灾中回响交错的图标

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.maze_buff_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.maze_buff_level


class RogueBuffGroup(ModelID):
    rogue_buff_group_id: typing.Annotated[int, pydantic.Field(validation_alias=aliases.ROGUE_BUFF_GROUP_ID)]
    rogue_buff_drop: typing.Annotated[list[int], pydantic.Field(validation_alias=aliases.ROGUE_BUFF_DROP)]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_buff_group_id


class RogueBuffType(ModelID):
    rogue_buff_type: int
    rogue_buff_type_textmap_id: Text
    rogue_buff_type_icon: str
    rogue_buff_type_title: Text
    rugue_buff_type_reward_quest_list: list[int]
    rogue_buff_type_sub_title: Text | None = None
    hint_desc: Text | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_buff_type


class UnlockNPCProgressID(Model):
    unlock_npc_id: typing.Annotated[int, pydantic.Field(validation_alias=aliases.UNLOCK_NPC_ID)]
    unlock_progress: typing.Annotated[int | None, pydantic.Field(validation_alias=aliases.UNLOCK_PROGRESS)] = None


class RogueDialogueDynamicDisplay(ModelID):
    display_id: int
    content_text: Text

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.display_id


class RogueDialogueOptionDisplay(ModelID):
    option_display_id: int
    option_title: Text | None = None
    option_desc: Text | None = None
    option_detail_desc: Text | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.option_display_id


class RogueEventSpecialOption(ModelID):
    special_option_id: int
    aeon_icon: str
    aeon_figure: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.special_option_id


class RogueHandBookEvent(ModelID):
    event_handbook_id: int
    unlock_npc_progress_id_list: list[UnlockNPCProgressID]
    event_title: Text
    event_type: Text
    event_reward: int
    order: int
    event_type_list: list[int]
    unlock_hint_desc: Text
    image_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.event_handbook_id


class RogueHandBookEventType(ModelID):
    rogue_hand_book_event_type: int
    rogue_event_type_title: Text
    type_icon: str
    activity_module_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_hand_book_event_type


class RogueHandbookMiracle(ModelID):
    """模拟宇宙奇物图鉴信息（解锁奖励、在哪些 DLC 中出现等）"""

    miracle_handbook_id: int
    miracle_reward: int
    miracle_type_list: list[int]
    miracle_display_id: int
    miracle_effect_display_id: int | None = None
    order: int
    miracle_id_for_effect_display: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.miracle_handbook_id


class RogueHandbookMiracleType(ModelID):
    """模拟宇宙奇物图鉴所属 DLC"""

    rogue_handbook_miracle_type: int
    rogue_miracle_type_title: Text
    type_icon: str
    activity_module_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_handbook_miracle_type


class RogueMiracle(ModelID):
    """模拟宇宙奇物"""

    miracle_id: int
    miracle_display_id: int | None = None  # 仅出现于 1.3 及之后
    miracle_effect_display_id: int | None = None  # 仅出现于 3.1 及之后
    unlock_id_list: list[int] | None = None  # 仅出现于 2.3 及之前
    use_effect: Text | None = None
    """无尽活动的特殊字段，之前之后都没有了"""
    is_show: bool = False
    miracle_reward: typing.Literal[106011] | None = None  # 仅出现于 1.6 及之前
    rogue_version: typing.Literal[1] | None = None  # 仅出现于 1.1 及之前
    unlock_handbook_miracle_id: int | None = None
    # 后面几个 1.2 之前的字段, 1.0 ~ 1.2 时候无 RogueMiracleDisplay.json, 全部塞在这个结构体里
    # 1.3 之后拆出 RogueMiracleDisplay.json 后便没有了, 2.6 ~ 3.0 短暂重新出现过但均为空，3.1 又没了
    miracle_name: Text | None = None  # 仅出现在 1.2 及之前
    miracle_desc: Text | None = None  # 仅出现在 1.2 及之前
    desc_param_list: list[Value[float]] | None = None  # 仅出现在 1.2 及之前
    miracle_bg_desc: Text | None = None  # 仅出现在 1.2 及之前
    miracle_tag: Text | None = None  # 仅出现在 1.2 及之前
    miracle_icon_path: str | None = None  # 仅出现在 1.2 及之前
    miracle_figure_icon_path: str | None = None  # 仅出现在 1.2 及之前
    extra_effect: list[int] | None = None  # 仅出现在 2.6 到 3.0，但均为空
    broken_change_miracle_id: int | None = None  # 2.3 及之后无此字段
    """损坏后会变成什么样, 目前看都是「乱七八糟的代码」系列奇物"""

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.miracle_id


class RogueMiracleDisplay(ModelID):
    """模拟宇宙奇物效果"""

    miracle_display_id: int
    miracle_name: Text
    miracle_desc: Text | None = None
    desc_param_list: list[Value[float]] | None = None
    extra_effect: list[int] | None = None
    miracle_bg_desc: Text | None = None
    miracle_tag: Text | None = None
    miracle_icon_path: str
    miracle_figure_icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.miracle_display_id


class RogueMiracleEffectDisplay(ModelID):
    """
    模拟宇宙奇物效果
    3.1 开始又移动部分字段到这里，RogueMiracleDisplay 对应字段消失
    """

    miracle_effect_display_id: int
    miracle_desc: Text | None = None
    miracle_simple_desc: Text | None = None
    desc_param_list: list[Value[float]]
    extra_effect: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.miracle_effect_display_id


class RogueMonster(ModelID):
    rogue_monster_id: int
    npc_monster_id: typing.Annotated[int, pydantic.Field(alias="NpcMonsterID")]
    event_id: int
    monster_drop_type: typing.Literal["AreaDrop"] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_monster_id


class RogueMonsterGroup(ModelID):
    rogue_monster_group_id: int
    rogue_monster_list_and_weight: dict[int, int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_monster_group_id


class RogueNPC(ModelID):
    rogue_npc_id: int
    npc_json_path: pathlib.Path

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_npc_id


class RogueTalkNameConfig(ModelID):
    talk_name_id: int
    name: Text
    sub_name: Text
    icon_path: str
    image_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.talk_name_id
