import enum
import typing

import pydantic
import typing_extensions

from .base import Element, Model, ModelID, Text


class IdentityType(enum.Enum):
    Normal = "AVATAR_IDENTITY_NORMAL"
    Master = "AVATAR_IDENTITY_MASTER"


class BodyType(enum.Enum):
    Boy = "BODY_BOY"
    Girl = "BODY_GIRL"
    Lady = "BODY_LADY"
    Loli = "BODY_LOLI"
    Male = "BODY_MALE"


class FightProp(enum.Enum):
    _ = "FIGHT_PROP_NONE"
    AttackPercent = "FIGHT_PROP_ATTACK_PERCENT"
    BaseAttack = "FIGHT_PROP_BASE_ATTACK"
    BaseDefense = "FIGHT_PROP_BASE_DEFENSE"
    BaseHP = "FIGHT_PROP_BASE_HP"
    ChargeEfficiency = "FIGHT_PROP_CHARGE_EFFICIENCY"
    Critical = "FIGHT_PROP_CRITICAL"
    CriticalHurt = "FIGHT_PROP_CRITICAL_HURT"
    ElementMastery = "FIGHT_PROP_ELEMENT_MASTERY"
    HPPercent = "FIGHT_PROP_HP_PERCENT"


class GrowCurve(enum.Enum):
    AttackS4 = "GROW_CURVE_ATTACK_S4"
    AttackS5 = "GROW_CURVE_ATTACK_S5"
    HPS4 = "GROW_CURVE_HP_S4"
    HPS5 = "GROW_CURVE_HP_S5"


class PropGrowCurve(Model):
    grow_curve: GrowCurve
    type: FightProp


class QualityType(enum.Enum):
    Orange = "QUALITY_ORANGE"
    OrangeSP = "QUALITY_ORANGE_SP"
    Purple = "QUALITY_PURPLE"


class WeaponType(enum.Enum):
    Bow = "WEAPON_BOW"
    Catalyst = "WEAPON_CATALYST"
    Claymore = "WEAPON_CLAYMORE"
    Pole = "WEAPON_POLE"
    SwordOneHand = "WEAPON_SWORD_ONE_HAND"


class UseType(enum.Enum):
    Abandon = "AVATAR_ABANDON"
    Formal = "AVATAR_FORMAL"
    SyncTest = "AVATAR_SYNC_TEST"
    Test = "AVATAR_TEST"


class Avatar(ModelID):
    animator_config_path_hash: Text
    attack_base: float
    avatar_identity_type: IdentityType
    """是否为主角，只有主角是 Master，其他为 Normal"""
    avatar_promote_id: int
    avatar_promote_reward_id_list: tuple[int, ...]
    avatar_promote_reward_level_list: tuple[int, ...]
    body_type: BodyType
    camp_id: typing.Annotated[typing.Literal[0], pydantic.Field(alias="campID")]
    cand_skill_depot_ids: tuple[int, ...]
    charge_efficiency: typing.Literal[1]
    combat_config_hash: Text
    controller_path_hash: Text
    controller_path_remote_hash: Text
    coop_pic_name_hash: Text
    critical: float
    critical_hurt: float
    defense_base: float
    deformation_mesh_path_hash: Text
    desc_text_map_hash: Text
    elec_sub_hurt: typing.Literal[0]
    element_mastery: int
    feature_tag_group_id: typing.Annotated[int, pydantic.Field(alias="featureTagGroupID")]
    fire_sub_hurt: typing.Literal[0]
    gacha_card_name_hash: Text
    gacha_image_name_hash: Text
    grass_sub_hurt: typing.Literal[0]
    hp_base: float
    ice_sub_hurt: typing.Literal[0]
    icon_name: str
    id_: int
    image_name: str
    initial_weapon: int
    is_range_attack: bool
    lod_pattern_name: typing.Literal[""]
    manekin_json_config_hash: Text
    manekin_motion_config: Text
    manekin_path_hash: Text
    name_text_map_hash: Text
    physical_sub_hurt: typing.Literal[0]
    prefab_path_hash: int
    prefab_path_ragdoll_hash: int
    prefab_path_remote_hash: int
    prop_grow_curves: tuple[PropGrowCurve, ...]
    quality_type: QualityType
    """星级，Purple 四星、Orange 五星，OrangeSP 只有埃洛伊"""
    rock_sub_hurt: typing.Literal[0]
    script_data_path_hash: Text
    side_icon_name: str
    skill_depot_id: int
    special_deformation_mesh_path_hash: Text
    stamina_recover_speed: typing.Literal[25]
    use_type: UseType
    water_sub_hurt: typing.Literal[0]
    weapon_type: WeaponType
    wind_sub_hurt: typing.Literal[0]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class DragType(enum.Enum):
    _ = "DRAG_NONE"
    RotateCamera = "DRAG_ROTATE_CAMERA"
    RotateCharacter = "DRAG_ROTATE_CHARACTER"


class NeedMonitor(enum.Enum):
    Never = "MONITOR_NEVER"
    OffStage = "MONITOR_OFF_STAGE"
    OnStage = "MONITOR_ON_STAGE"


class SpecialEnergy(enum.Enum):
    _ = "SPECIAL_ENERGY_NONE"
    Mavuika = "SPECIAL_ENERGY_MAVUIKA"
    Skirk = "SPECIAL_ENERGY_SKIRK"


SPECIAL_ENERGY_FIELD = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "IHFACGBENMJ",  # v6.0
        "MDCLPFMJPIP",  # v5.8
        "JKHIFIMMBCP",  # v5.7
        "FJIBJKLGEGJ",  # v5.6
        "PHGMFIGKKOH",  # v5.5
        "BNHEJBMOBLG",  # v5.4
        "GBCHEFKPKKG",  # v5.3
    )
)


class AvatarSkill(ModelID):
    ability_name: str
    buff_icon: str
    cd_slot: int
    cd_time: float
    cost_elem_type: Element | typing.Literal["None"]
    cost_elem_val: int
    cost_stamina: int
    desc_text_map_hash: Text
    drag_type: DragType
    energy_min: int
    extra_desc_text_map_hash: Text
    global_value_key: str
    id_: int
    is_attack_camera_lock: bool
    lock_shape: str
    lock_weight_params: tuple[float, ...]
    max_charge_num: int
    name_text_map_hash: Text
    need_monitor: NeedMonitor
    proud_skill_group_id: int
    share_cd_id: typing.Annotated[int, pydantic.Field(alias="shareCDID")]
    skill_icon: str
    special_energy: typing.Annotated[SpecialEnergy, SPECIAL_ENERGY_FIELD]
    trigger_id: typing.Annotated[int, pydantic.Field(alias="triggerID")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class InherentProudSkillOpens(Model):
    need_avatar_promote_level: typing.Literal[0, 1, 4]
    proud_skill_group_id: int


class Arkhe(enum.Enum):
    """始基力"""

    _ = "None"
    Furina = "Furina"
    """芙宁娜"""
    Ousia = "Ousia"
    """荒"""
    Pneuma = "Pneuma"
    """芒"""


ARKHE_FIELD = pydantic.Field(
    validation_alias=pydantic.AliasChoices(
        "JBEBHHPANFP",  # v6.0
        "LMKOLGFBOEN",  # v5.8
        "IHAHAINHGLF",  # v5.7
        "HKPHLGGKAKL",  # v5.6
        "CDKFLDLHCAD",  # v5.5
        "ILIINJLKPBD",  # v5.4
        "KKNGDMFNABI",  # v5.3
        "PADAKAFJEOL",  # v5.2
        "LENBICOFDEO",  # v5.1
        "BMODAPNPODN",  # v5.0
        "HGDEADIFCHM",  # v4.8
        "AIBFIHBNPIP",  # v4.7
        "HBOIHAAOLAM",  # v4.6
        "EOJOCCKGPFA",  # v4.5
        "GCIGNDHFAIK",  # v4.4
        "CJJBMDLNCCN",  # v4.3
        "EJMJBMIEPCF",  # v4.2
        "EDBAAACGADP",  # v4.0
    )
)


class AvatarSkillDepot(ModelID):
    arkhe: typing.Annotated[Arkhe, ARKHE_FIELD]
    attack_mode_skill: int
    energy_skill: int
    extra_abilities: tuple[typing.Literal[""], typing.Literal[""], typing.Literal[""]]
    id_: int
    inherent_proud_skill_opens: tuple[InherentProudSkillOpens, ...]
    leader_talent: int
    skill_depot_ability_group: str
    skills: tuple[int, ...]
    sub_skills: tuple[int, ...]
    talents: tuple[int, ...]
    talent_star_name: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
