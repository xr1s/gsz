import enum
import typing

import pydantic
import typing_extensions

from . import avatar
from .base import Element, ModelID, ModelMainSubID, Text, Value


class Quality(enum.Enum):
    Gold = "Gold"
    Prismatic = "Prismatic"
    Silver = "Silver"


class GridFightAugment(ModelID):
    id_: int
    category_id: int
    quality: Quality
    hex_name: Text
    hex_desc: Text
    desc_param_list: tuple[Value[float], ...]
    icon_path: str
    mini_icon_path: str
    chapter_limit_list: tuple[int, ...]
    is_o_c_effective: typing.Literal[1] | None = None
    json_path: str
    effect_param_list: tuple[Value[float], ...]
    augment_saved_value_list: tuple[str, ...]
    augment_game_ref_trait: tuple[int, ...]
    augment_game_ref_score: tuple[int, ...]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class GridFightBackRoleRank(ModelID):
    class PropertyType(enum.Enum):
        AllDamageTypeAddedRatio = "AllDamageTypeAddedRatio"
        AllDamageTypePenetrate = "AllDamageTypePenetrate"
        BreakDamageExtraAddedRatio = "BreakDamageExtraAddedRatio"
        ExtraAllDamageTypeAddedRatio3 = "ExtraAllDamageTypeAddedRatio3"
        HealRatioBase = "HealRatioBase"
        IcePenetrate = "IcePenetrate"
        SpeedAddedRatio = "SpeedAddedRatio"
        SPRatioBase = "SPRatioBase"
        StanceBreakAddedRatio = "StanceBreakAddedRatio"

    rank_id: int
    rank: int
    modify_energy_bar: Value[int] | None = None
    name: Text
    desc: Text
    icon_path: str
    trigger: Text
    owner_general_property_list: tuple[avatar.Property[PropertyType], ...]
    all_member_general_property_list: tuple[avatar.Property[PropertyType], ...]
    modify_skill_list: tuple[int, ...]
    rank_ability: tuple[str, ...]
    param: tuple[Value[float], ...]
    desc_param_list: tuple[float, ...]
    extra_effect_id_list: tuple[int, ...]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rank_id


class GridFightFrontSkill(ModelMainSubID):
    skill_id: int
    skill_name: Text | None = None
    skill_tag: Text
    skill_type_desc: Text
    level: int
    max_level: int
    skill_trigger_key: str
    skill_icon: str
    ultra_skill_icon: str
    level_up_cost_list: tuple[()]
    skill_desc: Text | None = None
    simple_skill_desc: Text | None = None
    rated_skill_tree_id: tuple[int, ...]
    rated_rank_id: tuple[int, ...]
    extra_effect_id_list: tuple[int, ...]
    simple_extra_effect_id_list: tuple[int, ...]
    show_stance_list: tuple[Value[int], ...]
    show_damage_list: tuple[()]
    show_heal_list: tuple[()]
    init_cool_down: typing.Literal[-1]
    cool_down: typing.Literal[-1]
    sp_base: Value[int] | None = None
    sp_need: Value[int] | None = None
    stance_damage_display: int | None = None
    sp_multiple_ratio: Value[float]
    b_p_add: Value[typing.Literal[1]] | None = None
    b_p_need: Value[int] | None = None
    delay_ratio: Value[typing.Literal[1]] | None = None
    param_list: tuple[Value[float], ...]
    simple_param_list: tuple[Value[float], ...]
    stance_damage_type: Element | None = None
    attack_type: avatar.AttackType | None = None
    skill_effect: avatar.SkillEffect
    hide_in_ui: bool = False

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.skill_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.level


class FrontBackType(enum.Enum):
    Back = "Back"
    Front = "Front"


class HealOrShieldDisplay(enum.Enum):
    Healer = "Healer"
    Shield = "Shield"


class ChargeType(enum.Enum):
    EnergyBar = "EnergyBar"
    MaxHP = "MaxHP"
    MaxSP = "MaxSP"
    Speed = "Speed"


class GridFightRoleBasicInfo(ModelID):
    id_: int
    avatar_id: int
    season_id_list: tuple[()]
    front_back_type: FrontBackType | None = None
    """None 为两者均可"""
    rarity: typing.Literal[1, 2, 3, 4, 5]
    heal_or_shield_display: HealOrShieldDisplay
    charge_type: tuple[ChargeType, ...]
    max_s_p_icon: str
    trait_list: tuple[int, ...]
    is_in_pool: typing.Literal[True]
    backend_rank_list: tuple[int, ...]
    equipment_id: int | None = None
    special_avatar_id: int
    season_id: typing.Literal[1]
    role_saved_value_list: tuple[str, ...]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class GridFightRoleSkillDisplay(ModelMainSubID):
    class CategoryTag(enum.Enum):
        Assist = "Assist"
        DPS = "DPS"
        Healer = "Healer"
        Shield = "Shield"

    role_id: int
    front_back_type: FrontBackType
    name: Text
    icon_path: str
    category_tag_list: tuple[CategoryTag, ...]

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.role_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        match self.front_back_type:
            case FrontBackType.Front:
                return 0
            case FrontBackType.Back:
                return 1


class GridFightRoleStar(ModelMainSubID):
    class PropertyType(enum.Enum):
        ExtraAllDamageTypeAddedRatio4 = "ExtraAllDamageTypeAddedRatio4"
        ExtraHPAddedRatio2 = "ExtraHPAddedRatio2"
        ExtraInitSP = "ExtraInitSP"
        ExtraSpeedAddedRatio2 = "ExtraSpeedAddedRatio2"

    id_: int
    star: int
    be_id: typing.Annotated[int, pydantic.Field(alias="BEID")]
    skill_override_src: tuple[int, ...]
    skill_override_dest: tuple[int, ...]
    front_show_skill_id_list: tuple[int, ...]
    front_one_word_desc: Text | None = None
    back_one_word_desc: Text | None = None
    back_ability_name: str
    back_param_list: tuple[Value[float], ...]
    json_override_config: str
    general_property_modify_list: tuple[avatar.Property[PropertyType], ...]
    show_stance_list: tuple[Value[int], ...]
    stance_damage_display: Value[typing.Literal[20]] | None = None
    back_energy_bar: Value[int] | None = None
    back_max_s_p: Value[int] | None = None
    back_initial_s_p: Value[int] | None = None
    back_initial_energy_bar: Value[int] | None = None
    front_power_base: Value[float]
    back_power_base: Value[float] | None = None
    luck_chance: Value[float]
    luck_damage: Value[typing.Literal[1]]
    extra_heal_base: Value[int]
    extra_shield_base: Value[int]
    be_skill_id_list: typing.Annotated[tuple[int, ...], pydantic.Field(alias="BESkillIDList")]
    back_show_skill_id_list: tuple[int, ...]

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.id_

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.id_


class TraitType(enum.Enum):
    Class = "Class"
    Unique = "Unique"


class GridFightTraitBasicInfo(ModelID):
    id_: int
    activation_type: typing.Literal["GreaterEqualThan"]
    trait_search_key: str
    icon_path: str
    mini_icon_path: str
    be_id_list: typing.Annotated[tuple[int, ...], pydantic.Field(alias="BEIDList")]
    trait_name: Text
    trait_type: TraitType | None = None
    """
    羁绊类型，分成三种
    None 是剧情羁绊（列车、天才、公司、仙舟等）
    Class 是战斗类型（群攻、燃血、击破、追击等）
    Unique 是五星角色特有单人羁绊
    """
    trait_effect_list: tuple[int, ...]
    trait_base_desc: Text
    trait_base_simple_desc: Text
    base_desc_param_list: tuple[Value[float], ...]
    cutin_path: str
    season_id: typing.Literal[1]
    trait_sort_priority: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
