import enum
import pathlib
import typing

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
    speed_modify_ratio: Value[float]  # 目前只有 1
    stance_modify_ratio: Value[float]  # 目前只有 1
    speed_modify_value: Value[float] = Value[float](value=0)  # 仅出现在 3.1
    stance_modify_value: Value[int] = Value[int](value=0)  # 仅出现在 3.1
    skill_list: list[int]
    summon_id_list: list[None]  # 目前只有空
    custom_values: list[CustomValue]
    dynamic_values: list[None]  # 目前只有空 []
    debuff_resist: list[DebuffResist]
    custom_value_tags: list[str]
    stance_weak_list: list[Element]
    damage_type_resistance: list[DamageTypeResistance]
    ability_name_list: list[str]
    override_ai_path: pathlib.Path
    override_ai_skill_sequence: list[AISkillSequence]
    override_skill_params: list[None]

    def id(self) -> int:
        return self.monster_id
