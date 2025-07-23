import enum
import pathlib
import typing

import pydantic
import typing_extensions

from .base import ModelID, Text, Value


class BuffRarity(enum.Enum):
    Normal = "Normal"
    Rare = "Rare"
    SuperRare = "SuperRare"
    VeryRare = "VeryRare"


class FateBuff(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="BGCDKMFDKLB")]
    class_trait_id: typing.Annotated[int, pydantic.Field(alias="GMGNOIACDJN")]
    skill_trait_id: typing.Annotated[int, pydantic.Field(alias="JOFAHBAPPIB")]
    unknow: typing.Annotated[tuple[()], pydantic.Field(alias="CEMMGMBGKNG")]
    icon: typing.Annotated[str, pydantic.Field(alias="IMCOKPODCIE")]
    rarity: typing.Annotated[BuffRarity, pydantic.Field(alias="JLKMNCOIDLG")]
    maze_buff: typing.Annotated[int, pydantic.Field(alias="DCBHNNDNHEO")]
    tag: typing.Annotated[Text, pydantic.Field(alias="OJOHNMAEMOP")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class Ability(enum.Enum):
    A = "A"
    AP = "A+"
    APP = "A++"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    EX = "EX"

    @typing_extensions.override
    def __str__(self) -> str:
        return self.value


class FateHandbookMaster(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="DJPCAIKIONP")]
    strength: typing.Annotated[Ability, pydantic.Field(alias="JJEMFAIELFN")]
    """筋力"""
    magical_energy: typing.Annotated[Ability, pydantic.Field(alias="ADAGFHGEKLD")]
    """魔力"""
    endurance: typing.Annotated[Ability, pydantic.Field(alias="HLGENJMDFOC")]
    """耐久"""
    luck: typing.Annotated[Ability, pydantic.Field(alias="BBKCBCEPIOM")]
    """幸运"""
    agility: typing.Annotated[Ability, pydantic.Field(alias="DBCLBBIMBMH")]
    """敏捷"""
    noble_phantasm: typing.Annotated[Ability, pydantic.Field(alias="ENDKMFOBHNF")]
    """宝具"""
    hougu_name: typing.Annotated[Text, pydantic.Field(alias="JFKAKNNMABK")]
    skill_comment: typing.Annotated[Text, pydantic.Field(alias="FGGIOCENNIA")]
    wish: typing.Annotated[Text, pydantic.Field(alias="DOABCFJBMKF")]
    story: typing.Annotated[Text, pydantic.Field(alias="NIMEAIDLEAA")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class Class(enum.Enum):
    Archer = "Archer"
    Assassin = "Assassin"
    Berserker = "Berserker"
    Caster = "Caster"
    Lancer = "Lancer"
    Rider = "Rider"
    Saber = "Saber"


class FateMaster(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="DJPCAIKIONP")]
    class_: typing.Annotated[Class, pydantic.Field(alias="FFAFMIFODFL")]
    config: typing.Annotated[str, pydantic.Field(alias="EEOHLAHCDEH")]
    skill_name: typing.Annotated[Text, pydantic.Field(alias="HLACJLFDGDD")]
    skill_desc: typing.Annotated[Text, pydantic.Field(alias="KADOICNKGAL")]
    skill_param: typing.Annotated[tuple[Value[float], ...], pydantic.Field(alias="HAIHCBBNIFL")]
    extra_effect: typing.Annotated[Text | None, pydantic.Field(alias="IILPOJFMPMD")] = None
    avatar: typing.Annotated[str, pydantic.Field(alias="GBBONBNFDGL")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class TalkWhen(enum.Enum):
    PostBattleOverviewLose = "PostBattleOverview_Lose"
    PostBattleOverviewLoseDead = "PostBattleOverview_Lose_Dead"
    PostBattleOverviewWin = "PostBattleOverview_Win"
    PostBattleOverviewWinRivalDead = "PostBattleOverview_Win_RivalDead"
    PostBattleVSLose = "PostBattleVS_Lose"
    PostBattleVSLoseDead = "PostBattleVS_Lose_Dead"
    PostBattleVSWin = "PostBattleVS_Win"
    PostBattleVSWinRivalDead = "PostBattleVS_Win_RivalDead"
    PreBattleOverview = "PreBattleOverview"
    PreBattleVS = "PreBattleVS"


class FateMasterTalk(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="MGBFCKPOHDD")]
    this_avatar_id: typing.Annotated[int, pydantic.Field(alias="KPKNMIDELCP")]
    this_avatar_talk: typing.Annotated[Text, pydantic.Field(alias="LCNGGPOILCF")]
    that_avatar_id: typing.Annotated[int | None, pydantic.Field(alias="NIHMKDADFFL")] = None
    that_avatar_talk: typing.Annotated[Text | None, pydantic.Field(alias="PLALJGHIEOD")] = None
    when: typing.Annotated[TalkWhen, pydantic.Field(alias="IKOMMBICGHC")]
    llephoelgda: typing.Annotated[tuple[()], pydantic.Field(alias="LLEPHOELGDA")]
    fkdjafnbekp: typing.Annotated[tuple[()], pydantic.Field(alias="FKDJAFNBEKP")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class ReijuCategory(enum.Enum):
    BondIncrease = "BondIncrease"
    BoundEnhance = "BoundEnhance"
    Economy = "Economy"
    PieceEnhance = "PieceEnhance"
    PieceIncrease = "PieceIncrease"
    ShopBuff = "ShopBuff"
    Speical = "Speical"


class FateReiju(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="BACDNAEHHIF")]
    days: typing.Annotated[tuple[int, ...], pydantic.Field(alias="LDDELFIJEOJ")]
    category: typing.Annotated[ReijuCategory, pydantic.Field(alias="FPMIPKECOHM")]
    name: typing.Annotated[Text, pydantic.Field(alias="AGEFEFBIGPG")]
    desc: typing.Annotated[Text, pydantic.Field(alias="BFJAIPNKMFD")]
    desc_simple: typing.Annotated[Text, pydantic.Field(alias="KDHBILHEONG")]
    params: typing.Annotated[tuple[Value[float], ...], pydantic.Field(alias="HAIHCBBNIFL")]
    current: typing.Annotated[Text | None, pydantic.Field(alias="IILPOJFMPMD")] = None
    unknow: typing.Annotated[tuple[()], pydantic.Field(alias="CEMMGMBGKNG")]
    config_path: typing.Annotated[pathlib.Path, pydantic.Field(alias="INKBBCOILNL")]
    maze_buff: typing.Annotated[int | None, pydantic.Field(alias="DCBHNNDNHEO")] = None
    corruption: typing.Annotated[int | None, pydantic.Field(alias="AFMIGHBGPBL")] = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class TraitType(enum.Enum):
    Class = "Clazz"
    Skill = "Skill"


class FateTrait(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="NGFFANDGNIL")]
    name: typing.Annotated[Text, pydantic.Field(alias="KBGACNHKLHI")]
    desc: typing.Annotated[Text, pydantic.Field(alias="GAABNPIDEAP")]
    desc_simple: typing.Annotated[Text, pydantic.Field(alias="HBIJEKNACIL")]
    params: typing.Annotated[tuple[Value[float], ...], pydantic.Field(alias="OIEKCNPMDFC")]
    current: typing.Annotated[Text | None, pydantic.Field(alias="IILPOJFMPMD")] = None
    buff: typing.Annotated[tuple[int, ...], pydantic.Field(alias="KGCJIHOHBPN")]
    avatar: typing.Annotated[int | None, pydantic.Field(alias="FJCLHHJBDDM")] = None
    """比如 Saber 关联到 Saber 自机角色, Archer 关联到 Archer 自机角色"""
    unknow_1: typing.Annotated[tuple[()], pydantic.Field(alias="CEMMGMBGKNG")]
    icons: typing.Annotated[tuple[str, ...], pydantic.Field(alias="JIPAHIICCJC")]
    icon: typing.Annotated[str, pydantic.Field(alias="HGMFEGIDCLI")]
    type_: typing.Annotated[TraitType, pydantic.Field(alias="COEOJHOLANO")]
    json_path: typing.Annotated[str, pydantic.Field(alias="MKEDMOLPMOC")]
    tag_1: typing.Annotated[Text, pydantic.Field(alias="HJNBJBBPIIM")]
    tag_2: typing.Annotated[Text | None, pydantic.Field(alias="BKAJGLKEGFB")] = None
    unknow_2: typing.Annotated[int | None, pydantic.Field(alias="AJIHNJGJLLJ")] = None
    category_icon: typing.Annotated[str, pydantic.Field(alias="GNGOLJIOFND")]
    video_caption: typing.Annotated[Text | None, pydantic.Field(alias="NAPCGMKCDFP")] = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class TraitBuffLevel(enum.Enum):
    Base = "Base"
    Extra01 = "Extra01"
    Extra02 = "Extra02"
    Extra03 = "Extra03"
    Extra04 = "Extra04"


class TraitBuffApplyType(enum.Enum):
    Additional = "Additional"
    Replace = "Replace"


class FateTraitBuff(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="IIMNAKFLOEH")]
    trait_id: typing.Annotated[int, pydantic.Field(alias="NGFFANDGNIL")]
    desc: typing.Annotated[Text, pydantic.Field(alias="BOPFKOKBGMP")]
    desc_simple: typing.Annotated[Text, pydantic.Field(alias="BBPDKIIGIAM")]
    params: typing.Annotated[tuple[Value[float], ...], pydantic.Field(alias="OIEKCNPMDFC")]
    unknow: typing.Annotated[Text | None, pydantic.Field(alias="IILPOJFMPMD")] = None
    level: typing.Annotated[TraitBuffLevel, pydantic.Field(alias="EAMAJGPCGFD")]
    apply_type: typing.Annotated[TraitBuffApplyType, pydantic.Field(alias="FCMAGJBLGOJ")]
    require: typing.Annotated[int, pydantic.Field(alias="OBBJIMJCCNO")]
    maze_buffs: typing.Annotated[list[int], pydantic.Field(alias="OLOJLHEKOPO")]
    json_path: typing.Annotated[str, pydantic.Field(alias="INKBBCOILNL")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
