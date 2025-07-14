import enum
import typing

import pydantic
import typing_extensions

from .base import ModelID, Text, Value


class Class(enum.Enum):
    Archer = "Archer"
    Assassin = "Assassin"
    Berserker = "Berserker"
    Caster = "Caster"
    Lancer = "Lancer"
    Rider = "Rider"
    Saber = "Saber"


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


class FateMaster(ModelID):
    id_: typing.Annotated[int, pydantic.Field(alias="DJPCAIKIONP")]
    class_: typing.Annotated[Class, pydantic.Field(alias="FFAFMIFODFL")]
    config: typing.Annotated[str, pydantic.Field(alias="EEOHLAHCDEH")]
    skill_name: typing.Annotated[Text, pydantic.Field(alias="HLACJLFDGDD")]
    skill_desc: typing.Annotated[Text, pydantic.Field(alias="KADOICNKGAL")]
    skill_param: typing.Annotated[list[Value[float]], pydantic.Field(alias="HAIHCBBNIFL")]
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
    llephoelgda: typing.Annotated[list[None], pydantic.Field(alias="LLEPHOELGDA")]
    fkdjafnbekp: typing.Annotated[list[None], pydantic.Field(alias="FKDJAFNBEKP")]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
