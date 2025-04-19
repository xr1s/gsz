import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import item
from .base import Model, ModelID, ModelMainSubID, ModelStringID, Text


class LandType(enum.Enum):
    Business = "Business"
    Exhibition = "Exhibition"
    Game = "Game"

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case LandType.Business:
                return "消费展区"
            case LandType.Exhibition:
                return "纪念展区"
            case LandType.Game:
                return "趣味展区"


class AvatarRarity(enum.Enum):
    Trainee = 1
    Journeyman = 2
    Senior = 3


class PlanetFesAvatar(ModelID):
    id_: int
    planet_type: LandType
    land_type: LandType
    rarity: AvatarRarity
    item_id: int
    cd: typing.Annotated[int, pydantic.Field(alias="CD")]
    skill_1_list: list[int]
    skill_2_list: list[int]
    income_param: typing.Literal[100]
    gacha_unlock_id_list: list[int]
    name: Text
    description: str
    head_icon: str
    mini_icon: str
    body: str
    anim_config: pathlib.Path
    mid_icon: str
    cargo_icon: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class PlanetFesAvatarEvent(ModelID):
    """二周年庆典活动访客事件"""

    id_: int
    unlock_id_list: list[int]
    event_option_id_list: list[int]
    avatar_id: int | None = None
    icon_path: str
    event_content: Text
    pic_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class PlanetFesAvatarEventOption(ModelID):
    event_option_id: int
    next_option_list: list[int]
    activity_reward_id: int | None = None
    reward_pool_id: int | None = None
    event_content: Text
    option_bubble_talk: Text

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.event_option_id


class Unit(enum.Enum):
    _ = ""
    K = "K"
    M = "M"
    B = "B"
    T = "T"
    AA = "AA"
    BB = "BB"
    CC = "CC"
    DD = "DD"
    EE = "EE"
    FF = "FF"
    GG = "GG"
    HH = "HH"
    II = "II"
    JJ = "JJ"
    KK = "KK"
    LL = "LL"
    MM = "MM"
    NN = "NN"
    OO = "OO"

    def __int__(self) -> int:
        return 1000 ** list(Unit).index(self)


class Num(Model):
    base_value: typing.Annotated[int, pydantic.Field(alias="base_value")]
    unit: typing.Annotated[Unit, pydantic.Field(alias="unit")] = Unit._

    def __int__(self) -> int:
        return self.base_value * int(self.unit)

    @typing_extensions.override
    def __str__(self) -> str:
        units = list(Unit)
        base_value = float(self.base_value)
        unit_index = units.index(self.unit)
        if base_value >= 1000:
            base_value /= 1000.0
            unit_index += 1
        unit = units[unit_index]
        return f"{base_value:.1f}".rstrip("0").removesuffix(".") + unit.value

    @staticmethod
    def from_int(num: int) -> "Num":
        units = iter(Unit)
        unit = next(units)
        while abs(num) >= 1000_000:
            num //= 1000
            unit = next(units)
        return Num(base_value=num, unit=unit)


class PlanetFesAvatarLevel(ModelID):
    level: int
    income_num: Num
    cost_num: Num
    grant_item_list: dict[int, int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.level


class PlanetFesAvatarRarity(ModelID):
    rarity: AvatarRarity
    income_param: int
    cost_param: int
    piece_transfer_num: int
    icon_path: str
    name: Text
    level_skip_star_up_detail: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> typing.Literal[1, 2, 3]:
        return self.rarity.value


class BuffType(enum.Enum):
    AllBonusEventIncomeIncrease = "AllBonusEventIncomeIncrease"
    AllEventIncomeIncrease = "AllEventIncomeIncrease"
    AllLandIncomeIncrease = "AllLandIncomeIncrease"
    AllLandIncomeIncreaseWithFesLevel = "AllLandIncomeIncreaseWithFesLevel"
    EventIncomeIncrease = "EventIncomeIncrease"
    IncomeIncreaseIfAvatarIdMatch = "IncomeIncreaseIfAvatarIdMatch"
    IncomeIncreaseIfLandTypeMatch = "IncomeIncreaseIfLandTypeMatch"
    IncomeIncreaseIfOnline = "IncomeIncreaseIfOnline"


class PlanetFesBuff(ModelID):
    id_: int
    source_id: int
    type: BuffType
    type_param: list[int]
    duration: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class PlanetFesBuffType(ModelStringID):
    id_: str
    decription: Text
    icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> str:
        return self.id_


class PlanetFesCard(ModelID):
    card_id: int
    rarity: typing.Literal[1, 2]
    name: Text
    description: Text
    pic_path: str
    piece_item_list: list[int]
    buff_id_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.card_id


class PlanetFesCardTheme(ModelID):
    theme_id: int
    card_id_list: list[int]
    name: Text
    icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.theme_id


class FinishType(enum.Enum):
    AcceptQuest = "PlanetFesAcceptQuest"
    ActivateCardNum = "PlanetFesActivateCardNum"
    AnyAvatarLevel = "PlanetFesAnyAvatarLevel"
    AnyAvatarLevelUpCnt = "PlanetFesAnyAvatarLevelUpCnt"
    AnyAvatarStar = "PlanetFesAnyAvatarStar"
    AvatarBuffEffectiveWithIDList = "PlanetFesAvatarBuffEffectiveWithIDList"
    AvatarDynamicLevel = "PlanetFesAvatarDynamicLevel"
    AvatarLevel = "PlanetFesAvatarLevel"
    AvatarNumWithLevel = "PlanetFesAvatarNumWithLevel"
    BuyLandInTypeList = "PlanetFesBuyLandInTypeList"
    ConsumeItemNumWithType = "PlanetFesConsumeItemNumWithType"
    CurCoinNum = "PlanetFesCurCoinNum"
    DeliverPamCargoCnt = "PlanetFesDeliverPamCargoCnt"
    DoGachaCnt = "PlanetFesDoGachaCnt"
    DoGachaInTypeList = "PlanetFesDoGachaInTypeList"
    DynamicProfitRate = "PlanetFesDynamicProfitRate"
    EffectiveAvatarBuffNum = "PlanetFesEffectiveAvatarBuffNum"
    FinishAvatarEventCnt = "PlanetFesFinishAvatarEventCnt"
    FinishBonusEventInTypeList = "PlanetFesFinishBonusEventInTypeList"
    FinishBusinessDayCnt = "PlanetFesFinishBusinessDayCnt"
    Level = "PlanetFesLevel"
    LevelCoinProgressPercent = "PlanetFesLevelCoinProgressPercent"
    MinWorkAvatarLevel = "PlanetFesMinWorkAvatarLevel"
    ProfitPerSecond = "PlanetFesProfitPerSecond"
    SetAvatarWorkCnt = "PlanetFesSetAvatarWorkCnt"
    SkillTreeAllLevel = "PlanetFesSkillTreeAllLevel"
    SkillTreePhase = "PlanetFesSkillTreePhase"
    UnlockAvatarInRarityList = "PlanetFesUnlockAvatarInRarityList"
    WorkAvatarDynamicLevel = "PlanetFesWorkAvatarDynamicLevel"


class ParamType(enum.Enum):
    Equal = "Equal"
    GreaterEqual = "GreaterEqual"
    ListContain = "ListContain"
    NoPara = "NoPara"


class PlanetFesFinishway(ModelID):
    id_: int
    finish_type: FinishType
    param_type: ParamType
    param_int_1: int | None = None
    param_int_2: int | None = None
    param_int_3: int | None = None
    param_str_1: str
    param_int_list: list[int]
    param_item_list: list[None]
    progress: int
    is_back_track: bool = False

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class RewardType(enum.Enum):
    Gold = "Gold"
    Gem = "Gem"


class PlanetFesGameRewardPool(ModelMainSubID):
    reward_pool_id: int
    order: int
    type: RewardType
    reward_param: dict[int, int]

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.reward_pool_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.order


class PlanetFesGameReward(ModelID):
    game_reward_id: int
    item_list: dict[int, int]
    buff_list: list[None]  # 始终为空串 []，可能是 2.0 一周年庆遗留下来的字段
    gold_num: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.game_reward_id


class PlanetFesLandType(ModelStringID):
    type: LandType
    name: Text
    icon_path: str
    big_buff_icon_path: str
    small_buff_icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> str:
        return self.type.value


class QuestType(enum.Enum):
    Achievement = "Achievement"
    Task = "Task"


class PlanetFesQuest(ModelID):
    id_: int
    quest_type: QuestType
    reward_item_list: list[item.Pair]
    finishway_id: int
    name: Text | None = None
    description: Text
    icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
