import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import aliases
from .base import Element, Model, ModelID, ModelMainSubID, Text, Value


class EliteGroup(ModelID):
    """精英组别，属性加成"""

    elite_group: int
    attack_ratio: Value[float]
    defence_ratio: Value[float]
    hp_ratio: Value[float]
    speed_ratio: Value[float]
    stance_ratio: Value[float]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.elite_group


class HardLevelGroup(ModelMainSubID):
    """敌方属性成长详情"""

    hard_level_group: int
    level: int
    attack_ratio: Value[float]
    defence_ratio: Value[float] = Value(value=1)
    hp_ratio: Value[float]
    speed_ratio: Value[float]
    stance_ratio: Value[float]
    combat_power_list: list[Value[int]]
    status_probability: Value[float] | None = None
    status_resistance: Value[float] | None = None

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.hard_level_group

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.level


class MonsterCamp(ModelID):
    """敌人阵营"""

    id_: int
    sort_id: int
    name: Text
    icon_path: str
    camp_type: typing.Literal["Monster"] = "Monster"  # 1.5 版本之后

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class CustomValue(Model):
    key: typing.Annotated[str, pydantic.Field(validation_alias=aliases.KEY)]
    val: typing.Annotated[int, pydantic.Field(validation_alias=aliases.VAL)] = 0


class Debuff(enum.Enum):
    Confine = "STAT_Confine"
    """禁锢"""
    Control = "STAT_CTRL"
    """控制"""
    Frozen = "STAT_CTRL_Frozen"
    """冻结"""
    Burn = "STAT_DOT_Burn"
    """灼烧"""
    Electric = "STAT_DOT_Electric"
    """触电"""
    Poison = "STAT_DOT_Poison"
    """风化"""
    Entangle = "STAT_Entangle"
    """纠缠"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case self.Confine:
                return "禁锢"
            case self.Control:
                return "控制"
            case self.Frozen:
                return "冻结"
            case self.Burn:
                return "灼烧"
            case self.Electric:
                return "触电"
            case self.Poison:
                return "风化"
            case self.Entangle:
                return "纠缠"


class DebuffResist(Model):
    """效果抵抗数值"""

    key: Debuff
    value: Value[float]


class DamageTypeResistance(Model):
    """元素抗性数值"""

    damage_type: Element
    value: Value[float]


class AISkillSequence(Model):
    id: typing.Annotated[int, pydantic.Field(validation_alias=aliases.ID)]


class MonsterConfig(ModelID):
    """敌人详情"""

    monster_name: Text
    monster_introduction: Text | None
    monster_strategy: list[None] | None  # 仅出现于 3.4 版本及之后
    monster_id: int
    monster_template_id: int
    monster_battle_introduction: Text | None = None  # 仅出现于 1.0
    hard_level_group: int = 1  # 仅出现在 3.2 版本及之前，全部都是 1
    elite_group: int
    attack_modify_ratio: Value[float]
    defence_modify_ratio: Value[float] = Value[float](value=1)
    hp_modify_ratio: Value[float]
    speed_modify_ratio: Value[typing.Literal[1]]
    stance_modify_ratio: Value[typing.Literal[1]]
    speed_modify_value: Value[float] = Value[float](value=0)  # 仅出现在 3.1
    stance_modify_value: Value[int] = Value[int](value=0)  # 仅出现在 3.1
    skill_list: list[int]
    summon_id_list: list[int] | None = None  # 仅出现于 3.1 版本及之后；3.1 版本均为空，3.2 起出现数据
    custom_values: list[CustomValue]
    dynamic_values: list[None]  # 目前只有空 []
    debuff_resist: list[DebuffResist]
    custom_value_tags: list[str]
    stance_weak_list: list[Element]
    damage_type_resistance: list[DamageTypeResistance]
    ability_name_list: list[str]
    override_ai_path: pathlib.Path
    override_ai_skill_sequence: list[AISkillSequence]
    override_skill_params: list[None] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.monster_id


class MonsterSkillConfig(ModelID):
    """敌人技能"""

    skill_id: int
    skill_name: Text
    icon_path: str
    skill_desc: Text
    skill_type_desc: Text
    skill_tag: Text | None = None  # 仅出现于 1.1 版本及之后
    phase_list: list[int]
    is_threat: bool = False
    """是否大招（游戏中详情页展示为渐变红底）"""
    extra_effect_id_list: list[int]
    damage_type: Element | None = None
    """技能伤害元素，非攻击技能为 None"""
    skill_trigger_key: str
    sp_hit_base: Value[int] | None = None
    """敌方攻击施放后，会给命中角色增加多少充能。非攻击技能为 None"""
    delay_ratio: Value[float] | None = None
    param_list: list[Value[float]]
    attack_type: typing.Literal["Normal"]
    ai_cd: typing.Annotated[typing.Literal[1], pydantic.Field(alias="AI_CD")] = 1  # 仅出现于 3.2 版本及之前
    ai_icd: typing.Annotated[typing.Literal[1], pydantic.Field(alias="AI_ICD")] = 1  # 仅出现于 3.2 版本及之前
    modifier_list: list[str] = []  # 2.0 无此字段

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.skill_id


class Rank(enum.Enum):
    BigBoss = "BigBoss"
    """周本 Boss"""
    Elite = "Elite"
    """精英敌人"""
    LittleBoss = "LittleBoss"
    """剧情 Boss"""
    Minion = "Minion"
    """普通敌人，目前总共就 21 种，不清楚和 MinionLv2 的区别"""
    MinionLv2 = "MinionLv2"
    """普通敌人，大多是这种，不清楚和 Minion 的区别"""


class MonsterTemplateConfig(ModelID):
    """
    敌人模板
    对应一种敌人类型
    不同的敌人类型可能是同一个种族，但是数值上会有差异
    种族大概就是 group_id 相同的 template，指建模头像相同的敌人
    """

    monster_template_id: int
    monster_strategy: list[None] | None = None  # 仅出现于 3.4 版本及之后
    template_group_id: int | None = None  # 敌人种族 ID
    release_in_atlas: bool = False
    atlas_sort_id: int | None = None
    monster_name: Text
    monster_camp_id: int | None = None
    monster_base_type: typing.Literal[""] = ""  # 仅出现于 3.2 版本及之前
    rank: Rank
    json_config: pathlib.Path
    icon_path: str
    round_icon_path: str
    image_path: str
    prefab_path: str
    manikin_prefab_path: str
    manikin_config_path: pathlib.Path
    manikin_image_path: str | None = None  # 仅出现于 1.2 版本及之后
    nature_id: typing.Literal[1] = 1  # 仅出现于 3.2 版本及之前
    attack_base: Value[float]
    defence_base: Value[int] = Value(value=1)
    hp_base: Value[float]
    speed_base: Value[int] | None = None
    stance_base: Value[int] | None = None
    stance_type: Element | None = None
    critical_damage_base: Value[float] | None = None
    status_resistance_base: Value[float] | None = None
    minimum_fatigue_ratio: Value[float]
    speed_modify_value: Value[int] | None = None
    stance_modify_value: Value[int] | None = None
    ai_path: pathlib.Path
    stance_count: int | None = None
    initial_delay_ratio: Value[float] | None = None
    ai_skill_sequence: list[AISkillSequence]
    npc_monster_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.monster_template_id


class NPCMonsterData(ModelID):
    """
    站在大世界的敌人信息（`MonsterConfig` 等都是入战后的敌人信息）
    """

    id_: int
    npc_name: Text | None = None
    prefab_path: str | None = None  # 仅出现在 1.1 及之前
    config_entity_path: pathlib.Path
    npc_icon_path: str
    npc_title: Text | None = None
    board_show_list: list[typing.Literal[2]]
    json_path: pathlib.Path
    default_ai_path: pathlib.Path
    character_type: typing.Literal["NPCMonster"]
    sub_type: typing.Literal["Monster"]
    mini_map_icon_type: typing.Literal[5] | None = None
    rank: Rank
    is_maze_link: bool = False
    prototype_id: int
    mapping_info_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
