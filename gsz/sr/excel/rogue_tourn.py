import enum
import pathlib
import typing

import pydantic
import typing_extensions

from .base import (
    FIELD_ALIASES_ROGUE_WEEKLY_TYP,
    FIELD_ALIASES_ROGUE_WEEKLY_VAL,
    Model,
    ModelID,
    ModelMainSubID,
    Text,
)
from .rogue import BuffCategory, Path


class RogueTournBuff(ModelMainSubID):
    """模拟宇宙祝福"""

    maze_buff_id: int
    maze_buff_level: int
    """最高就是 1，强化后祝福"""
    rogue_buff_type: int
    rogue_buff_category: BuffCategory | None = None
    rogue_buff_tag: int
    extra_effect_id_list: list[int]
    unlock_display: int
    is_in_handbook: bool = False

    @property
    @typing_extensions.override
    def main_id(self) -> int:
        return self.maze_buff_id

    @property
    @typing_extensions.override
    def sub_id(self) -> int:
        return self.maze_buff_level


class TestPath(enum.Enum):
    """某次不小心把测试数据露到线上导致的"""

    Preservation = "test_Preservation"
    """存护"""
    Remembrance = "test_Remembrance"
    """记忆"""
    Nihility = "test_Nihility"
    """虚无"""
    Abundance = "test_Abundance"
    """丰饶"""
    TheHunt = "test_TheHunt"
    """巡猎"""
    Destruction = "test_Destruction"
    """毁灭"""
    Elation = "test_Elation"
    """欢愉"""
    Propagation = "test_Propagation"
    """繁育"""
    Erudition = "test_Erudition"
    """智识"""


class RogueTournBuffType(ModelID):
    rogue_buff_type: int
    rogue_buff_type_name: Text
    rogue_buff_type_title: Text | None = None
    rogue_buff_type_sub_title: Text | None = None
    rogue_buff_type_deco_name: Path | TestPath
    rogue_buff_type_icon: str
    rogue_buff_type_small_icon: str
    rogue_buff_type_large_icon: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.rogue_buff_type


class RogueTournContentDisplay(ModelID):
    display_id: int
    display_content: Text

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.display_id


class Mode(enum.Enum):
    TournMode1 = "Tourn1"
    """人间喜剧"""
    TournMode2 = "Tourn2"
    """千面英雄"""


class FormulaCategory(enum.Enum):
    """方程稀有度"""

    Rare = "Rare"
    """一星方程"""
    Epic = "Epic"
    """二星方程"""
    Legendary = "Legendary"
    """三星方程"""
    PathEcho = "PathEcho"
    """临界方程"""

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case self.Rare:
                return "1星"
            case self.Epic:
                return "2星"
            case self.Legendary:
                return "3星"
            case self.PathEcho:
                return "4星"


class RogueTournFormula(ModelID):
    formula_id: int
    tourn_mode: Mode | None = None
    main_buff_type_id: int
    """主要命途"""
    main_buff_num: int
    """激活方程需求主要命途祝福的数量"""
    sub_buff_type_id: int | None = None
    """次要命途，临界方程时无次要命途"""
    sub_buff_num: int | None = None
    """激活方程需求次要命途祝福的数量，临界方程时无次要命途"""
    formula_category: FormulaCategory
    """方程稀有度"""
    maze_buff_id: int
    """方程对应增益"""
    formula_display_id: int
    formula_icon: str | None = None
    """方程主要命途图标"""
    formula_sub_icon: str | None = None
    """方程次要命途图标，临界方程时图标使用 ultra_formula_icon 字段"""
    is_in_handbook: bool = False
    ultra_formula_icon: str | None = None  # 仅出现在 3.0 及之前
    """临界方程命途图标"""
    formula_story_json: pathlib.Path
    """临界方程和三星方程首次展开的推演（千面英雄方程此字段均为空）"""
    unlock_display_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.formula_id


class RogueTournFormulaDisplay(ModelID):
    formula_display_id: int
    formula_type_display: int | None = None
    formula_story: Text
    extra_effect: list[int]
    handbook_unlock_display_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.formula_display_id


class MiracleCategory(enum.Enum):
    Common = "Common"
    """一星奇物"""
    Rare = "Rare"
    """二星奇物"""
    Legendary = "Legendary"
    """三星奇物"""
    Hex = "Hex"
    """加权奇物"""
    Negative = "Negative"
    """负面奇物"""

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case self.Common:
                return "1星"
            case self.Rare:
                return "2星"
            case self.Legendary:
                return "3星"
            case self.Hex:
                return "加权奇物"
            case self.Negative:
                return "负面奇物"


class RogueTournHandbookMiracle(ModelID):
    """
    差分宇宙奇物图鉴

    和奇物确实会有区别
    比如天彗合金不同型号不会出现在图鉴
    比如「绝对失败处方」、「塔奥牌」等根据选择会有多种不同效果
    这一类奇物具体介绍只会在 RogueTournHandbookMiracle 里，不同效果只会在 RogueTournMiracle 里
    """

    handbook_miracle_id: int
    miracle_display_id: int
    miracle_effect_display_id: int | None = None
    miracle_category: MiracleCategory
    unlock_desc: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.handbook_miracle_id


class RogueTournMiracle(ModelID):
    """差分宇宙奇物"""

    miracle_id: int
    tourn_mode: Mode
    miracle_category: MiracleCategory
    miracle_display_id: int
    miracle_effect_display_id: int | None = None
    handbook_miracle_id: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.miracle_id


class TitanType(enum.Enum):
    Ianos = "Ianos"
    Moneta = "Moneta"
    Nikadory = "Nikadory"
    Phageina = "Phageina"
    Xenatos = "Xenatos"
    Zagreus = "Zagreus"


class BlessBattleDisplayCategory(enum.Enum):
    Day = "Day"
    Night = "Night"


class RogueTournTitanBless(ModelID):
    """金血祝颂"""

    titan_bless_id: int
    titan_type: TitanType
    titan_bless_level: int
    maze_buff_id: int
    extra_effect_id_list: list[int]
    bless_ratio: int | None = None
    bless_battle_display_category_list: list[BlessBattleDisplayCategory] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.titan_bless_id


class RogueTournWeeklyChallenge(ModelID):
    """周期演算"""

    challenge_id: int
    weekly_name: Text
    weekly_content_list: list[int]
    weekly_content_detail_list: list[int]
    reward_id: int
    display_final_monster_groups: dict[typing.Literal["0"], int]
    display_monster_groups_1: dict[typing.Literal["0", "3"], int]
    display_monster_groups_2: dict[typing.Literal["0", "3"], int]
    display_monster_groups_3: dict[typing.Literal["0"], int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.challenge_id


class DescParamType(enum.Enum):
    """周期演算中预设套装的物品分类"""

    Formula = "Formula"
    """方程"""
    Miracle = "Miracle"
    """奇物"""
    TitanBless = "TitanBless"
    """金血祝颂"""


class DescParam(Model):
    type: typing.Annotated[DescParamType, pydantic.Field(validation_alias=FIELD_ALIASES_ROGUE_WEEKLY_TYP)]
    value: typing.Annotated[int, pydantic.Field(validation_alias=FIELD_ALIASES_ROGUE_WEEKLY_VAL)]


class RogueTournWeeklyDisplay(ModelID):
    weekly_display_id: int
    weekly_display_content: Text
    desc_params: list[DescParam]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.weekly_display_id
