import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import item
from .base import Element, Model, ModelID, ModelMainSubID, Path, Text, Value

CHANGE_INFO_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "GMLBHCFGKJM",  # v3.8
        "OELNFIJLCOL",  # v3.1
        "IGHDLNOGKLC",  # v3.0
        "IJJNCPBDOKC",  # v2.7
        "GFLIIILGPNC",  # v2.6
        "IAOOCGHKJKO",  # v2.5
        "AGLEDDHKMIG",  # v2.4
        "LFGAHGEPDCM",  # v2.3
        "OMIKHCAPMCE",  # v2.2
        "FPLIGJFHEML",  # v2.1
    )
)
CHANGE_INFO_UNLOCK = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "GACICPLOKNF",  # v3.8
        "CCOFCKBMMMI",  # v3.1
        "LDNIPIFDOPM",  # v3.0
        "HHKNJLIBFLL",  # v2.7
        "DMONIBLMMFE",  # v2.6
        "JFDJOPDLOEM",  # v2.5
        "IGOAHDGINJM",  # v2.4
        "JGNNNABJJMB",  # v2.3
        "DFLGNAAJAFO",  # v2.2
        "AJPOMMJGGFH",  # v2.1
    )
)
CHANGE_AVATAR_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "EKGLJCKKFFP",  # v3.8
        "DJPCAIKIONP",  # v3.1
        "KOBDFDHBFGN",  # v3.0
        "NJIKGMAJKPM",  # v2.7
        "JMFFPFCPKBF",  # v2.6
        "APJPKOHBLJJ",  # v2.5
        "ALADBMFHHNG",  # v2.4
        "GBDKFBOIGOG",  # v2.3
        "LNAJBIGNEME",  # v2.2
        "ADLMEHJMHNH",  # v2.1
    )
)
CHANGE_CAMP_ID = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "ADLEONICBGO",  # v3.8
        "EBBHGBKEPAA",  # v3.1
        "DLKMBMBEOIA",  # v3.0
        "APHCIBECBLI",  # v2.7
        "KKHPKDKGKGA",  # v2.6
        "IFMNLHOPJGB",  # v2.5
        "LFDFBPHFLIN",  # v2.4
        "DGONPAMLHBG",  # v2.3
        "NDALFKFDLHD",  # v2.2
        "MADANDKCGCM",  # v2.1
    )
)


class AtlasAvatarChangeInfo(ModelID):
    id_: typing.Annotated[int, CHANGE_INFO_ID]
    unlock: typing.Annotated[int, CHANGE_INFO_UNLOCK]
    avatar_id: typing.Annotated[int, CHANGE_AVATAR_ID]
    camp_id: typing.Annotated[int, CHANGE_CAMP_ID]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class AvatarAtlas(ModelID):
    avatar_id: int
    default_unlock: bool = False
    gacha_schedule: typing.Literal["", "2023-06-28  12:00:00", "2023-05-17 18:00:00"] = ""  # 仅出现于 1.1 及之前
    is_local_time: bool = False  # 仅出现于 1.1 及之前
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


class ManikinCharacterConfig(Model):
    class Axis(Model):
        x: float = 0
        y: float = 0
        z: float = 0

    # 仅出现于 3.0 及之前，3.0 及之前仅有 typ 字段
    typ: typing.Literal["RPG.GameCore.ManikinCharacterConfig"] = "RPG.GameCore.ManikinCharacterConfig"
    character_body_size: CharacterBodySize | None = None  # None 是成男体型
    free_style_character_id: str | None = None
    free_style_character_config_path: pathlib.Path | None = None
    talk_emotion_asset_path: str | None = None
    anim_event_config_list: tuple[pathlib.Path, ...]
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
    avatar_initial_skin_name: Text | None = None  # 仅出现于 3.0 及之前，仅有空值（找不到 TextMap 的 Text）
    avatar_initial_skin_desc: Text | None = None  # 仅出现于 3.0 及之前，仅有空值（找不到 TextMap 的 Text）
    json_path: pathlib.Path
    damage_type: Element
    sp_need: Value[int] | None = None  # 仅有遐蝶 SP 是 None
    exp_group: typing.Literal[1]
    max_promotion: typing.Literal[6]
    max_rank: typing.Literal[6] = 6
    rank_id_list: tuple[int, ...]
    reward_list: tuple[item.Pair, ...] | None = None
    reward_list_max: tuple[item.Pair, ...] | None = None  # 仅出现在 3.1 及之前
    skill_list: tuple[int, ...]
    avatar_base_type: Path
    default_avatar_model_path: str
    default_avatar_head_icon_path: str
    avatar_side_icon_path: str
    avatar_mini_icon_path: str
    avatar_gacha_result_img_path: str | None = None  # 仅出现于 1.3 及之后
    action_avatar_head_icon_path: str
    ultra_skill_cut_in_prefab_path: str
    ui_avatar_model_path: str
    manikin_json_path: pathlib.Path
    avatar_desc: Text | None = None  # 仅出现于 3.0 及之前，仅有空值（找不到 TextMap 的 Text）
    ai_path: str
    skilltree_prefab_path: str
    damage_type_resistance: tuple[()]
    release: bool = False
    side_avatar_head_icon_path: str
    waiting_avatar_head_icon_path: str
    avatar_cutin_img_path: str
    avatar_cutin_bg_img_path: typing.Annotated[str, pydantic.Field(alias="AvatarCutinBgImgPath")]
    avatar_cutin_front_img_path: str
    avatar_cutin_intro_text: Text | None = None
    gacha_result_offset: tuple[float, ...] | None = None  # 仅出现于 1.2 及之前
    avatar_drop_offset: tuple[float, ...]
    avatar_trial_offset: tuple[float, ...]
    player_card_offset: tuple[float, ...]
    assist_offset: tuple[float, ...]
    assist_bg_offset: typing.Annotated[tuple[float, ...], pydantic.Field(alias="AssistBgOffset")]
    avatar_self_show_offset: tuple[float, ...]

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
    promotion_cost_list: tuple[item.Pair, ...]
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
    extra_effect_id_list: tuple[int, ...] | None = None  # 仅出现于 2.6 及之后
    icon_path: str
    skill_add_level_list: dict[int, int]
    rank_ability: tuple[str, ...]
    unlock_cost: tuple[item.Pair, ...]
    param: tuple[Value[float], ...]

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
    level_up_cost_list: tuple[()] | None = None
    skill_desc: Text | None = None
    simple_skill_desc: Text | None = None
    rated_skill_tree_id: tuple[int, ...]
    rated_rank_id: tuple[int, ...]
    extra_effect_id_list: tuple[int, ...]
    simple_extra_effect_id_list: tuple[int, ...]
    show_stance_list: tuple[Value[int], ...]
    show_damage_list: tuple[()] | None = None
    show_heal_list: tuple[()] | None = None
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
    param_list: tuple[Value[float], ...]
    simple_param_list: tuple[Value[float], ...]
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
    MainCharacter = 5
    """记忆主专属技能"""


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
    Point21 = "Point21"
    """记忆主专属技能"""


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


_P = typing.TypeVar("_P", bound=enum.Enum)


class Property(Model, typing.Generic[_P]):
    property_type: _P
    value: Value[float] = Value(value=0)


class AvatarSkillTreeConfig(ModelMainSubID):
    point_id: int
    level: int
    avatar_id: int
    enhanced_id: typing.Literal[1] | None = None
    point_type: PointType
    anchor_type: typing.Annotated[
        AnchorType, pydantic.Field(validation_alias=pydantic.AliasChoices("AnchorType", "Anchor"))
    ]
    max_level: typing.Literal[1, 10, 6]
    default_unlock: bool = False
    pre_point: tuple[int, ...]
    status_add_list: tuple[Property[PropertyType], ...]
    material_list: tuple[item.Pair, ...]
    avatar_level_limit: int | None = None
    avatar_promotion_limit: int | None = None
    level_up_skill_id: tuple[int, ...]
    icon_path: str
    point_name: Text
    point_desc: Text
    simple_point_desc: typing.Literal[""] | None = None  # 仅出现于 2.5 及之后
    extra_effect_id_list: tuple[int, ...] | None = None  # 仅出现于 2.5 及之后
    simple_extra_effect_id_list: tuple[()] | None = None  # 仅出现于 2.5 及之后
    recommend_priority: typing.Literal[1, 2, 3] | None = None
    ability_name: str
    point_trigger_key: PointTriggerKey | Text
    param_list: tuple[Value[float], ...]

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
    # 仅出现于 3.0 及之前，仅有空值（找不到 TextMap 的 Text）
    voice_f: typing.Annotated[Text | None, pydantic.Field(alias="Voice_F")] = None
    audio_id: int | None = None
    is_battle_voice: bool = False
    audio_event: str
    mouth_anim_path: typing.Literal[""] = ""  # 仅出现于 2.0 及之前
    unlock: int | None = None
    unlock_desc: Text | None = None  # 仅出现于 2.3 及之前
    sort_id: int | None = None  # 仅出现于 1.5 及之后
    replace_id: int | None = None

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.avatar_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.voice_id
