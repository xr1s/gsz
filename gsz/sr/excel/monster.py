import enum
import pathlib
import typing

import pydantic
import pydantic

from .base import Element, ID_ALIASES, KEY_ALIASES, Model, Text, VAL_ALIASES, Value


class EliteGroup(Model):
    """精英组别，属性加成"""

    elite_group: int
    attack_ratio: Value[float]
    defence_ratio: Value[float]
    hp_ratio: Value[float]
    speed_ratio: Value[float]
    stance_ratio: Value[float]

    def id(self) -> int:
        return self.elite_group


class HardLevelGroup(Model):
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

    def main_id(self) -> int:
        return self.hard_level_group

    def sub_id(self) -> int:
        return self.level


class CustomValue(Model):
    key: typing.Annotated[str, pydantic.Field(validation_alias=KEY_ALIASES)]
    val: typing.Annotated[int, pydantic.Field(validation_alias=VAL_ALIASES)] = 0


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


class DebuffResist(Model):
    """效果抵抗数值"""

    key: Debuff
    value: Value[float]


class DamageTypeResistance(Model):
    """元素抗性数值"""

    damage_type: Element
    value: Value[float]


class AISkillSequence(Model):
    id: typing.Annotated[int, pydantic.Field(validation_alias=ID_ALIASES)]


class MonsterConfig(Model):
    """敌人详情"""

    monster_id: int
    monster_template_id: int
    monster_name: Text
    monster_introduction: Text | None
    monster_battle_introduction: Text | None = None  # 仅出现于 1.0
    hard_level_group: int
    elite_group: int
    attack_modify_ratio: Value[float]
    defence_modify_ratio: Value[float] = Value[float](value=1)
    hp_modify_ratio: Value[float]
    speed_modify_ratio: Value[typing.Literal[1]]
    stance_modify_ratio: Value[typing.Literal[1]]
    speed_modify_value: Value[float] = Value[float](value=0)  # 仅出现在 3.1
    stance_modify_value: Value[int] = Value[int](value=0)  # 仅出现在 3.1
    skill_list: list[int]
    summon_id_list: list[None] | None = None  # 目前只有空
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

    def id(self) -> int:
        return self.monster_id


class MonsterSkillConfig(Model):
    """敌人技能"""

    skill_id: int
    skill_name: Text
    icon_path: str
    skill_desc: Text
    skill_type_desc: Text
    skill_tag: Text
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
    ai_cd: typing.Annotated[typing.Literal[1], pydantic.Field(alias="AI_CD")]
    ai_icd: typing.Annotated[typing.Literal[1], pydantic.Field(alias="AI_ICD")]
    modifier_list: list[str] = []  # 2.0 无此字段

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


class MonsterTemplateConfig(Model):
    """
    敌人模板
    对应一种敌人类型
    不同的敌人类型可能是同一个种族，但是数值上会有差异
    种族是我自创的概念，游戏中没用，指建模头像相同的敌人
    """

    monster_template_id: int
    template_group_id: int | None = None  # 敌人种族 ID
    release_in_atlas: bool = False
    atlas_sort_id: int | None = None
    monster_name: Text
    monster_camp_id: int | None = None
    monster_base_type: typing.Literal[""]
    rank: Rank
    json_config: pathlib.Path
    icon_path: str
    round_icon_path: str
    image_path: str
    prefab_path: str
    manikin_prefab_path: str
    manikin_config_path: pathlib.Path
    manikin_image_path: str
    nature_id: typing.Literal[1]
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

    def id(self) -> int:
        return self.monster_template_id
