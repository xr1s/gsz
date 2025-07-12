import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import item
from .base import Element, Model, ModelID, ModelMainSubID, Path, Text, Value


class AtlasAvatarChangeInfo(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="OELNFIJLCOL")]
    unlock: typing.Annotated[int, pydantic.Field(alias="CCOFCKBMMMI")]
    avatar_id: typing.Annotated[int, pydantic.Field(alias="DJPCAIKIONP")]
    camp_id: typing.Annotated[int, pydantic.Field(alias="EBBHGBKEPAA")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class AvatarAtlas(ModelID):
    avatar_id: int
    default_unlock: bool = False
    cv_cn: typing.Annotated[Text, pydantic.Field(alias="CV_CN")]
    cv_jp: typing.Annotated[Text, pydantic.Field(alias="CV_JP")]
    cv_kr: typing.Annotated[Text, pydantic.Field(alias="CV_KR")]
    cv_en: typing.Annotated[Text | None, pydantic.Field(alias="CV_EN")] = None
    camp_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.avatar_id


class AvatarCamp(ModelID):
    id_: int
    sort_id: int
    name: Text
    icon_path: typing.Literal[""]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class Rarity(enum.Enum):
    Type4 = "CombatPowerAvatarRarityType4"
    Type5 = "CombatPowerAvatarRarityType5"


class CharacterBodySize(enum.Enum):
    Boy = "Boy"
    """少年"""
    Girl = "Girl"
    """少女"""
    Kid = "Kid"
    """幼女"""
    Lad = "Lad"
    """男青年"""
    Lady = "Lady"
    """成女"""
    Maid = "Maid"
    """女青年"""
    Miss = "Miss"
    """星"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case CharacterBodySize.Boy:
                return "少年"
            case CharacterBodySize.Girl:
                return "少女"
            case CharacterBodySize.Kid:
                return "幼女"
            case CharacterBodySize.Lad:
                return "男青年"
            case CharacterBodySize.Lady:
                return "成女"
            case CharacterBodySize.Maid:
                return "女青年"
            case CharacterBodySize.Miss:
                return "星"


class ManikinAvatar(Model):
    class Axis(Model):
        x: float
        y: float
        z: float

    character_body_size: CharacterBodySize | None = None  # None 是成男体型
    free_style_character_id: str | None = None
    free_style_character_config_path: pathlib.Path | None = None
    talk_emotion_asset_path: str | None = None
    anim_event_config_list: list[pathlib.Path]
    rotations_by_index: dict[int, Axis] | None = None
    eidolon_position: Axis | None = None
    positions_by_name: dict[str, Axis] | None = None


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
    reward_list: list[item.Pair] | None = None
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
    manikin_json_path: pathlib.Path
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


class AvatarPlayerIcon(ModelID):
    id_: int
    image_path: str
    is_visible: bool = False
    avatar_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class AvatarPromotionConfig(ModelMainSubID):
    avatar_id: int
    promotion: int | None = None
    promotion_cost_list: list[item.Pair]
    max_level: int
    player_level_require: typing.Literal[15] | None = None
    world_level_require: typing.Literal[1, 2, 3, 4, 5] | None = None
    attack_base: Value[float]
    attack_add: Value[float]
    defence_base: Value[float]
    defence_add: Value[float]
    hp_base: Value[float]
    hp_add: Value[float]
    speed_base: Value[int]
    critical_chance: Value[float]
    critical_damage: Value[float]
    base_aggro: Value[int]

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.avatar_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.promotion if self.promotion is not None else 0


class AvatarRankConfig(ModelID):
    rank_id: int
    rank: typing.Literal[1, 2, 3, 4, 5, 6]
    trigger: Text
    name: Text
    desc: Text
    extra_effect_id_list: list[int]
    icon_path: str
    skill_add_level_list: dict[int, int]
    rank_ability: list[str]
    unlock_cost: list[item.Pair]
    param: list[Value[float]]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rank_id


class SkillTriggerKey(enum.Enum):
    _ = ""
    Skill01 = "Skill01"
    Skill02 = "Skill02"
    Skill03 = "Skill03"
    Skill11 = "Skill11"
    Skill12 = "Skill12"
    Skill13 = "Skill13"
    Skill14 = "Skill14"
    Skill21 = "Skill21"
    Skill22 = "Skill22"
    Skill23 = "Skill23"
    Skill31 = "Skill31"
    Skill32 = "Skill32"
    Skill33 = "Skill33"
    Skill34 = "Skill34"
    SkillMaze = "SkillMaze"
    SkillP01 = "SkillP01"
    SkillP02 = "SkillP02"
    SkillP03 = "SkillP03"
    SkillP04 = "SkillP04"


class AttackType(enum.Enum):
    BPSkill = "BPSkill"
    Maze = "Maze"
    MazeNormal = "MazeNormal"
    Normal = "Normal"
    Ultra = "Ultra"
    Servant = "Servant"


class SkillEffect(enum.Enum):
    AoEAttack = "AoEAttack"
    Blast = "Blast"
    Bounce = "Bounce"
    Defence = "Defence"
    Enhance = "Enhance"
    Impair = "Impair"
    MazeAttack = "MazeAttack"
    Restore = "Restore"
    SingleAttack = "SingleAttack"
    Summon = "Summon"
    Support = "Support"


class AvatarSkillConfig(ModelMainSubID):
    skill_id: int
    skill_name: Text
    skill_tag: Text
    skill_type_desc: Text
    level: int
    max_level: int
    skill_trigger_key: SkillTriggerKey
    skill_icon: str
    ultra_skill_icon: str
    level_up_cost_list: list[None] | None = None
    skill_desc: Text | None = None
    simple_skill_desc: Text | None = None
    rated_skill_tree_id: list[int]
    rated_rank_id: list[int]
    extra_effect_id_list: list[int]
    simple_extra_effect_id_list: list[int]
    show_stance_list: list[Value[int]]
    show_damage_list: list[None] | None = None
    show_heal_list: list[None] | None = None
    init_cool_down: typing.Literal[-1] = -1
    cool_down: typing.Literal[-1] = -1
    sp_base: Value[int] | None = None
    sp_need: Value[int] | None = None
    stance_damage_display: int | None = None
    sp_multiple_ratio: Value[float]
    bp_need: typing.Annotated[Value[int] | None, pydantic.Field(alias="BPNeed")] = None
    skill_need: Text | None = None
    bp_add: typing.Annotated[Value[typing.Literal[1]] | None, pydantic.Field(alias="BPAdd")] = None
    delay_ratio: Value[typing.Literal[1]]
    param_list: list[Value[float]]
    simple_param_list: list[Value[float]]
    stance_damage_type: Element | None = None
    attack_type: AttackType | None = None
    skill_effect: SkillEffect
    hide_in_ui: bool = False
    skill_combo_value_delta: Value[int] | None = None

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.skill_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.level


class PointType(enum.Enum):
    StatBonus = 1
    """属性加成"""
    Skill = 2
    """技能：普攻、战技、终结技、天赋、秘技"""
    BonusAbility = 3
    """天赋"""
    Memosprite = 4
    """忆灵相关"""


class AnchorType(enum.Enum):
    Point01 = "Point01"
    Point02 = "Point02"
    Point03 = "Point03"
    Point04 = "Point04"
    Point05 = "Point05"
    Point06 = "Point06"
    Point07 = "Point07"
    Point08 = "Point08"
    Point09 = "Point09"
    Point10 = "Point10"
    Point11 = "Point11"
    Point12 = "Point12"
    Point13 = "Point13"
    Point14 = "Point14"
    Point15 = "Point15"
    Point16 = "Point16"
    Point17 = "Point17"
    Point18 = "Point18"
    Point19 = "Point19"
    Point20 = "Point20"


class PointTriggerKey(enum.Enum):
    PointB1 = "PointB1"
    PointB2 = "PointB2"
    PointB3 = "PointB3"
    PointBPSkill = "PointBPSkill"
    PointMaze = "PointMaze"
    PointNormal = "PointNormal"
    PointPassive = "PointPassive"
    PointS1 = "PointS1"
    PointS10 = "PointS10"
    PointS2 = "PointS2"
    PointS3 = "PointS3"
    PointS4 = "PointS4"
    PointS5 = "PointS5"
    PointS6 = "PointS6"
    PointS7 = "PointS7"
    PointS8 = "PointS8"
    PointS9 = "PointS9"
    PointServant1 = "PointServant1"
    PointServant2 = "PointServant2"
    PointUltra = "PointUltra"


class PropertyType(enum.Enum):
    AttackAddedRatio = "AttackAddedRatio"
    BreakDamageAddedRatioBase = "BreakDamageAddedRatioBase"
    CriticalChanceBase = "CriticalChanceBase"
    CriticalDamageBase = "CriticalDamageBase"
    DefenceAddedRatio = "DefenceAddedRatio"
    FireAddedRatio = "FireAddedRatio"
    HPAddedRatio = "HPAddedRatio"
    IceAddedRatio = "IceAddedRatio"
    ImaginaryAddedRatio = "ImaginaryAddedRatio"
    PhysicalAddedRatio = "PhysicalAddedRatio"
    QuantumAddedRatio = "QuantumAddedRatio"
    SpeedDelta = "SpeedDelta"
    StatusProbabilityBase = "StatusProbabilityBase"
    StatusResistanceBase = "StatusResistanceBase"
    ThunderAddedRatio = "ThunderAddedRatio"
    WindAddedRatio = "WindAddedRatio"

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911, PLR0912
        match self:
            case PropertyType.AttackAddedRatio:
                return "攻击"
            case PropertyType.BreakDamageAddedRatioBase:
                return "击破"
            case PropertyType.CriticalChanceBase:
                return "暴击率"
            case PropertyType.CriticalDamageBase:
                return "暴击伤害"
            case PropertyType.DefenceAddedRatio:
                return "防御"
            case PropertyType.FireAddedRatio:
                return "火"
            case PropertyType.HPAddedRatio:
                return "生命"
            case PropertyType.IceAddedRatio:
                return "冰"
            case PropertyType.ImaginaryAddedRatio:
                return "虚数"
            case PropertyType.PhysicalAddedRatio:
                return "物理"
            case PropertyType.QuantumAddedRatio:
                return "量子"
            case PropertyType.SpeedDelta:
                return "速度"
            case PropertyType.StatusProbabilityBase:
                return "效果命中"
            case PropertyType.StatusResistanceBase:
                return "效果抵抗"
            case PropertyType.ThunderAddedRatio:
                return "雷"
            case PropertyType.WindAddedRatio:
                return "风"

    def wiki_value(self, value: float) -> str:
        match self:
            case (
                PropertyType.AttackAddedRatio
                | PropertyType.BreakDamageAddedRatioBase
                | PropertyType.CriticalChanceBase
                | PropertyType.CriticalDamageBase
                | PropertyType.DefenceAddedRatio
                | PropertyType.FireAddedRatio
                | PropertyType.HPAddedRatio
                | PropertyType.IceAddedRatio
                | PropertyType.ImaginaryAddedRatio
                | PropertyType.PhysicalAddedRatio
                | PropertyType.QuantumAddedRatio
                | PropertyType.StatusProbabilityBase
                | PropertyType.StatusResistanceBase
                | PropertyType.ThunderAddedRatio
                | PropertyType.WindAddedRatio
            ):
                return str(round(value * 100, 1))
            case PropertyType.SpeedDelta:
                return str(round(value))


class StatusAdd(Model):
    property_type: PropertyType
    value: Value[float]


class AvatarSkillTreeConfig(ModelMainSubID):
    point_id: int
    level: int
    avatar_id: int
    enhanced_id: typing.Literal[1] | None = None
    point_type: PointType
    anchor_type: AnchorType
    max_level: typing.Literal[1, 10, 6]
    default_unlock: bool = False
    pre_point: list[int]
    status_add_list: list[StatusAdd]
    material_list: list[item.Pair]
    avatar_level_limit: int | None = None
    avatar_promotion_limit: int | None = None
    level_up_skill_id: list[int]
    icon_path: str
    point_name: Text
    point_desc: Text
    simple_point_desc: typing.Literal[""]
    extra_effect_id_list: list[int]
    simple_extra_effect_id_list: list[None]
    recommend_priority: typing.Literal[1, 2, 3] | None = None
    ability_name: str
    point_trigger_key: PointTriggerKey
    param_list: list[Value[float]]

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.point_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.level


class StoryAtlas(ModelMainSubID):
    avatar_id: int
    story_id: int
    story: Text
    unlock: int | None = None
    replace_id: int | None = None
    sort_id: int | None = None

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.avatar_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.story_id


class VoiceAtlas(ModelMainSubID):
    avatar_id: int
    voice_id: int
    voice_title: Text
    voice_m: typing.Annotated[Text, pydantic.Field(alias="Voice_M")]
    audio_id: int | None = None
    is_battle_voice: bool = False
    audio_event: str
    unlock: int | None = None
    sort_id: int
    replace_id: int | None = None

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.avatar_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.voice_id
