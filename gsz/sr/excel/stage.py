import enum
import pathlib
import typing

import pydantic
import typing_extensions

from . import aliases
from .base import Model, ModelID, Text, Value


class Type(enum.Enum):
    AetherDivide = "AetherDivide"
    BattleCollege = "BattleCollege"
    BoxingClub = "BoxingClub"
    Challenge = "Challenge"
    ClockParkActivity = "ClockParkActivity"
    Cocoon = "Cocoon"
    ElationActivity = "ElationActivity"
    EvolveBuildActivity = "EvolveBuildActivity"
    FantasticStory = "FantasticStory"
    FarmElement = "FarmElement"
    FateActivity = "FateActivity"
    FeverTimeActivity = "FeverTimeActivity"
    FightActivity = "FightActivity"
    FightFest = "FightFest"
    GridFightActivity = "GridFightActivity"
    Heliobus = "Heliobus"
    LocalLegend = "LocalLegend"
    Mainline = "Mainline"
    PunkLord = "PunkLord"
    RogueChallengeActivity = "RogueChallengeActivity"
    RogueEndlessActivity = "RogueEndlessActivity"
    RogueRelic = "RogueRelic"
    StarFightActivity = "StarFightActivity"
    StrongChallengeActivity = "StrongChallengeActivity"
    SummonActivity = "SummonActivity"
    SwordTraining = "SwordTraining"
    TelevisionActivity = "TelevisionActivity"
    TreasureDungeon = "TreasureDungeon"
    Trial = "Trial"
    TrialAdventure = "TrialAdventure"
    VerseSimulation = "VerseSimulation"


class DataKey(enum.Enum):
    BattleCondition = "_BattleCondition"
    BattlePerformStage = "_BattlePerformStage"
    BattleTarget = "_BattleTarget"
    BGM = "_BGM"
    BindingMazeBuff = "_BindingMazeBuff"
    ChallengeStoryType = "_ChallengeStoryType"
    CloseBattleStartDialog = "_CloseBattleStartDialog"
    CreateBattleActionEvent = "_CreateBattleActionEvent"
    CreateBattleEvent = "_CreateBattleEvent"
    DeferCreateTrialPlayer = "_DeferCreateTrialPlayer"
    EnsureTeamAliveKey = "_EnsureTeamAliveKey"
    IsEliteBattle = "_IsEliteBattle"
    Load3DTextFromFloor = "_Load3DTextFromFloor"
    MainMonster = "_MainMonster"
    SpecialBattleStartCamera = "_SpecialBattleStartCamera"
    StageBannedAvatarID = "_StageBannedAvatarID"
    StageInfiniteGroup = "_StageInfiniteGroup"
    Wave = "_Wave"


class Data(Model):
    key: typing.Annotated[DataKey, pydantic.Field(validation_alias=aliases.KEY)]
    val: typing.Annotated[str, pydantic.Field(validation_alias=aliases.VAL)]


class SubLevelGraph(Model):
    key: typing.Annotated[typing.Literal["_DefaultSubStage"], pydantic.Field(validation_alias=aliases.KEY)]
    unknown_0: typing.Annotated[str, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKNOW0)]
    unknown_1: typing.Annotated[str | None, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKNOW1)] = None
    unknown_2: typing.Annotated[str | None, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKOWN2)] = None
    unknown_3: typing.Annotated[str | None, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKOWN3)] = None
    unknown_4: typing.Annotated[str | None, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKOWN4)] = None
    unknown_5: typing.Annotated[str | None, pydantic.Field(validation_alias=aliases.STAGE_SUBLEVELGRAPH_UNKOWN5)] = None


class StageConfig(ModelID):
    stage_id: int
    stage_type: Type
    stage_name: Text
    hard_level_group: int
    level: int
    elite_group: int | None = None
    level_graph_path: pathlib.Path
    stage_ability_config: list[str]
    battle_scoring_group: int | None = None
    sub_level_graphs: list[SubLevelGraph]
    stage_config_data: list[Data]
    monster_list: list[list[int]]
    level_lose_condition: list[str]
    level_win_condition: list[str]
    forbid_auto_battle: bool = False
    forbid_view_mode: bool = False
    release: bool = False
    forbid_exit_battle: bool = False
    monster_warning_ratio: float | None = None
    reset_battle_speed: bool = False
    trial_avatar_list: list[int] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.stage_id

    @pydantic.field_validator("monster_list", mode="before")
    @classmethod
    def __monster_list_validator(cls, value: list[dict[str, int]]) -> list[list[int]]:  # pyright: ignore[reportUnusedFunction]
        monster_list = [[0 for _ in monsters] for monsters in value]
        for item, monsters in zip(monster_list, value, strict=True):
            for key, monster in monsters.items():
                index = int(key.removeprefix("Monster"))
                item[index - 1] = monster
        return monster_list

    @pydantic.field_serializer("monster_list")
    @classmethod
    def __monster_list_serializer(cls, value: list[list[int]]) -> list[dict[str, int]]:  # pyright: ignore[reportUnusedFunction]
        monster_list: list[dict[str, int]] = [{} for _ in value]
        for item, monsters in zip(monster_list, value, strict=True):
            for index, monster in enumerate(monsters):
                key = f"Monster{index + 1}"
                item[key] = monster
        return monster_list


class StageInfiniteGroup(ModelID):
    wave_group_id: int
    wave_id_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.wave_group_id


class StageInfiniteMonsterGroup(ModelID):
    infinite_monster_group_id: int
    monster_list: list[int]
    elite_group: int | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.infinite_monster_group_id


class StageInfiniteWaveConfig(ModelID):
    infinite_wave_id: int
    monster_group_id_list: list[int]
    max_monster_count: int
    max_teammate_count: int
    ability: str
    param_list: list[Value[float]]
    clear_previous_ability: typing.Literal[True]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.infinite_wave_id
