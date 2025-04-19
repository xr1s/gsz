import enum
import typing

import pydantic

from ...excel import Path, Value, item
from . import target
from .base import BaseModel, Custom, FixedValue, Model, get_discriminator


class AdvByCompareDimensionID(Model):
    pass


class AdvByEntitiesExist(Model):
    pass


class AdvByEntityExist(Model):
    target_type: target.Target


class AdvByFastDeliverHasMultiRoute(Model):
    pass


class AdvByPlayerInVisionZone(Model):
    pass


class AdventureByCompareMP(Model):
    pass


class AdventureByPropInPosition(Model):
    pass


class AdventureByPropShowInfoId(Model):
    pass


class AdventureIsTriggerBattleByNpcMonster(Model):
    pass


class ByAdvCharacterLogicState(Model):
    pass


class ByAnd(Model):
    predicate_list: list["Predicate"]
    inverse: bool = False


class ByAny(Model):
    predicate_list: list["Predicate"]


class ByAnyNpcMonsterInRange(Model):
    pass


class ByCheckColonyTrace(Model):
    colony_id: FixedValue[int]
    inverse: bool = False


class ByCheckDarkTeamDestroy(Model):
    pass


class ByCheckFloorCustomBool(Model):
    name: Value[str]
    inverse: bool = False


class ByCheckTimelineEntityState(Model):
    pass


class ByCheckTrialCharacterDie(Model):
    pass


class ByCheckLineupHeroAvatarID(Model):
    pass


class ByCompareCarryMazebuff(Model):
    pass


class ByCompareCurrentTeammemberCount(Model):
    pass


class ByCompareCustomString(Model):
    pass


class ByCompareDynamicValue(Model):
    pass


class ByCompareEventMissionState(Model):
    pass


class CompareType(enum.Enum):
    Equal = "Equal"
    Greater = "Greater"
    GreaterEqual = "GreaterEqual"
    Less = "Less"
    LessEqual = "LessEqual"
    NotEqual = "NotEqual"


class ByCompareFloorCustomFloat(Model):
    name: Value[str] | Custom
    compare_type: CompareType
    compare_value: FixedValue[int]


class ByCompareFloorCustomFloatV2(Model):
    name: Value[str]
    compare_type: CompareType
    compare_value: FixedValue[int]


class ByCompareFloorCustomString(Model):
    pass


class ByCompareFloorSavedValueV2(Model):
    name: str
    compare_type: CompareType
    compare_value: int


class ByCompareFloorSavedValue(Model):
    name: str | None = None
    dynamic_name: Value[str] | None = None
    compare_type: CompareType | None = None
    compare_value: int | None = None
    inverse: bool = True


class ByCompareGraphDynamicFloat(Model):
    pass


class ByCompareGraphDynamicString(Model):
    pass


class ByCompareGroupMonsterNumByState(Model):
    pass


class ByCompareGroupState(Model):
    pass


class ByCompareHeartDialTracingNPC(Model):
    inverse: bool = False


class ByCompareHPRatio(Model):
    pass


class ByCompareIsBookAvailable(Model):
    pass


class ByCompareIsWolfBroBulletActivated(Model):
    pass


class ByCompareItemNum(Model):
    item_pair: list[item.Pair]
    inverse: bool = False


class ByCompareItemNumber(Model):
    item_id: FixedValue[int]
    number: FixedValue[int]
    compare_type: CompareType


class MissionState(enum.Enum):
    Started = "Started"
    Finish = "Finish"


class ByCompareMainMissionState(Model):
    main_mission_id: int
    main_mission_state: MissionState | None = None
    all_story_line: bool = False
    inverse: bool = False


class ByCompareMissionBattleWin(Model):
    pass


class MissionCustomValue(BaseModel):
    index: int | None = None
    is_local: typing.Annotated[bool, pydantic.Field(alias="isLocal")] = False
    is_range: typing.Annotated[bool, pydantic.Field(alias="isRange")] = False
    valid_value_param_list: list[int] | None = None


class ByCompareMissionCustomValue(Model):
    class MissionCustomValueCompare(BaseModel):
        index: int
        is_local: typing.Annotated[typing.Literal[True], pydantic.Field(alias="isLocal")]
        valid_value_param_list: list[int]

    main_mission_id: int
    mission_custom_value: MissionCustomValue
    equation_type: CompareType | None = None
    show_compare_value: bool = False
    target_value: int | None = None
    mission_custom_value_compare: MissionCustomValueCompare | None = None


class ByCompareMusicRhythmSongID(Model):
    pass


class ByCompareNPCMonsterCheckState(Model):
    pass


class ByComparePerformance(Model):
    performance_id: int
    inverse: bool = False


class ByComparePerformanceResult(Model):
    compare_type: CompareType
    compare_value: int


class ByComparePropAnimState(Model):
    pass


class PropState(enum.Enum):
    BridgeState1 = "BridgeState1"
    BridgeState2 = "BridgeState2"
    BridgeState3 = "BridgeState3"
    BridgeState4 = "BridgeState4"
    CheckPointDisable = "CheckPointDisable"
    CheckPointEnable = "CheckPointEnable"
    ChestClosed = "ChestClosed"
    ChestLocked = "ChestLocked"
    ChestUsed = "ChestUsed"
    CustomState01 = "CustomState01"
    CustomState02 = "CustomState02"
    CustomState03 = "CustomState03"
    CustomState04 = "CustomState04"
    CustomState05 = "CustomState05"
    CustomState06 = "CustomState06"
    CustomState07 = "CustomState07"
    CustomState08 = "CustomState08"
    Destructed = "Destructed"
    Elevator1 = "Elevator1"
    Elevator2 = "Elevator2"
    EventClose = "EventClose"
    EventOpen = "EventOpen"
    Hidden = "Hidden"
    Locked = "Locked"
    Open = "Open"
    TriggerDisable = "TriggerDisable"
    TriggerEnable = "TriggerEnable"
    WaitActive = "WaitActive"


class ByComparePropState(Model):
    target_type: target.Target
    state: PropState | None = None
    inverse: bool = False


class ByComparePropStateNumber(Model):
    pass


class ByCompareQuestGetReward(Model):
    quest_id: FixedValue[int]
    inverse: bool = False


class ByCompareQuestProgress(Model):
    quest_id: FixedValue[int]
    progress: FixedValue[int]
    equation_type: CompareType


class ByCompareRogueMode(Model):
    pass


class ByCompareRogueTournLevel(Model):
    pass


class ByCompareRogueTournPermanantTalentState(Model):
    pass


class ByCompareRotatableRegionLoadingState(Model):
    pass


class ByCompareSeriesID(Model):
    pass


class ByCompareServerSubMissionState(Model):
    pass


class ByCompareStageType(Model):
    pass


class ByCompareStoryLineID(Model):
    target_story_line_id: int | None = None


class ByCompareSubMissionState(Model):
    sub_mission_id: int | None = None
    sub_mission_state: MissionState | None = None
    all_story_line: bool = False
    inverse: bool = False


class ByCompareTeamLeaderBodySize(Model):
    pass


class ByCompareTeamLeaderPath(Model):
    path_type: Path


class ByCompareTextJoinValue(Model):
    text_join_id: int
    value: int


class ByCompareVersionFinalMainMission(Model):
    main_mission_id: int


class ByCompareWaveCount(Model):
    pass


class ByContainBehaviorFlag(Model):
    pass


class ByContainCustomString(Model):
    pass


class ByDeployPuzzleBasePointIsAnswer(Model):
    pass


class ByDistance(Model):
    pass


class ByHasInsertAbilityPending(Model):
    pass


class ByHasInsertBattlePerform(Model):
    pass


class ByHasUnGottenLevelReward(Model):
    pass


class Gender(enum.Enum):
    Man = "GENDER_MAN"
    Woman = "GENDER_WOMAN"


class ByHeroGender(Model):
    gender: Gender


class ByIfGroupIsOccupied(Model):
    pass


class ByInTrackCameraByPathID(Model):
    pass


class ByIsActivityInSchedule(Model):
    pass


class ByIsContainAdventureModifier(Model):
    pass


class ByIsContainModifier(Model):
    pass


class ByIsEraFlipperEntityShow(Model):
    pass


class ByIsEvolveBuildCountDownItemShow(Model):
    pass


class ByIsGenderType(Model):
    pass


class ByIsInDistrict(Model):
    pass


class ByIsInfiniteBattle(Model):
    pass


class ByIsRotatableTimeRewindTarget(Model):
    pass


class ByIsShowInActionBar(Model):
    pass


class ByIsSwordTrainingSkillCanLearn(Model):
    pass


class ByIsTargetValid(Model):
    pass


class ByIsTutorialFinish(Model):
    pass


class ByIsUIPageOpen(Model):
    pass


class ByLevelLoseCheck(Model):
    pass


class ByLocalPlayerAvatarID(Model):
    avatar_ids: typing.Annotated[list[int], pydantic.Field(alias="AvatarIDs")]


class ByLocalPlayerIsFakeAvatar(Model):
    pass


class ByLocalPlayerIsHero(Model):
    pass


class ByMainMissionFinish(Model):
    pass


class ByNot(Model):
    predicate: "Predicate"


class BySimulateSpeedUp(Model):
    pass


class ByTargetAliveCheck(Model):
    pass


class ByTargetListIntersects(Model):
    pass


class ByTargetNpcExists(Model):
    group_id: int
    group_npc_id: int


class ByTimeRewindTargetMotionPause(Model):
    pass


class ConvinceByCompareHp(Model):
    compare_type: CompareType
    compare_value: int


class PropPredicateWithEntity(Model):
    pass


Predicate = typing.Annotated[
    typing.Annotated[AdvByCompareDimensionID, pydantic.Tag("AdvByCompareDimensionID")]
    | typing.Annotated[AdvByEntitiesExist, pydantic.Tag("AdvByEntitiesExist")]
    | typing.Annotated[AdvByEntityExist, pydantic.Tag("AdvByEntityExist")]
    | typing.Annotated[AdvByFastDeliverHasMultiRoute, pydantic.Tag("AdvByFastDeliverHasMultiRoute")]
    | typing.Annotated[AdvByPlayerInVisionZone, pydantic.Tag("AdvByPlayerInVisionZone")]
    | typing.Annotated[AdventureByCompareMP, pydantic.Tag("AdventureByCompareMP")]
    | typing.Annotated[AdventureByPropInPosition, pydantic.Tag("AdventureByPropInPosition")]
    | typing.Annotated[AdventureByPropShowInfoId, pydantic.Tag("AdventureByPropShowInfoId")]
    | typing.Annotated[AdventureIsTriggerBattleByNpcMonster, pydantic.Tag("AdventureIsTriggerBattleByNpcMonster")]
    | typing.Annotated[ByAdvCharacterLogicState, pydantic.Tag("ByAdvCharacterLogicState")]
    | typing.Annotated[ByAnd, pydantic.Tag("ByAnd")]
    | typing.Annotated[ByAny, pydantic.Tag("ByAny")]
    | typing.Annotated[ByAnyNpcMonsterInRange, pydantic.Tag("ByAnyNpcMonsterInRange")]
    | typing.Annotated[ByCheckColonyTrace, pydantic.Tag("ByCheckColonyTrace")]
    | typing.Annotated[ByCheckDarkTeamDestroy, pydantic.Tag("ByCheckDarkTeamDestroy")]
    | typing.Annotated[ByCheckFloorCustomBool, pydantic.Tag("ByCheckFloorCustomBool")]
    | typing.Annotated[ByCheckTimelineEntityState, pydantic.Tag("ByCheckTimelineEntityState")]
    | typing.Annotated[ByCheckTrialCharacterDie, pydantic.Tag("ByCheckTrialCharacterDie")]
    | typing.Annotated[ByCheckLineupHeroAvatarID, pydantic.Tag("ByCheckLineupHeroAvatarID")]
    | typing.Annotated[ByCompareCarryMazebuff, pydantic.Tag("ByCompareCarryMazebuff")]
    | typing.Annotated[ByCompareCurrentTeammemberCount, pydantic.Tag("ByCompareCurrentTeammemberCount")]
    | typing.Annotated[ByCompareCustomString, pydantic.Tag("ByCompareCustomString")]
    | typing.Annotated[ByCompareDynamicValue, pydantic.Tag("ByCompareDynamicValue")]
    | typing.Annotated[ByCompareEventMissionState, pydantic.Tag("ByCompareEventMissionState")]
    | typing.Annotated[ByCompareFloorCustomFloat, pydantic.Tag("ByCompareFloorCustomFloat")]
    | typing.Annotated[ByCompareFloorCustomFloatV2, pydantic.Tag("ByCompareFloorCustomFloatV2")]
    | typing.Annotated[ByCompareFloorCustomString, pydantic.Tag("ByCompareFloorCustomString")]
    | typing.Annotated[ByCompareFloorSavedValue, pydantic.Tag("ByCompareFloorSavedValue")]
    | typing.Annotated[ByCompareFloorSavedValueV2, pydantic.Tag("ByCompareFloorSavedValueV2")]
    | typing.Annotated[ByCompareGraphDynamicFloat, pydantic.Tag("ByCompareGraphDynamicFloat")]
    | typing.Annotated[ByCompareGraphDynamicString, pydantic.Tag("ByCompareGraphDynamicString")]
    | typing.Annotated[ByCompareGroupMonsterNumByState, pydantic.Tag("ByCompareGroupMonsterNumByState")]
    | typing.Annotated[ByCompareGroupState, pydantic.Tag("ByCompareGroupState")]
    | typing.Annotated[ByCompareHeartDialTracingNPC, pydantic.Tag("ByCompareHeartDialTracingNPC")]
    | typing.Annotated[ByCompareHPRatio, pydantic.Tag("ByCompareHPRatio")]
    | typing.Annotated[ByCompareIsBookAvailable, pydantic.Tag("ByCompareIsBookAvailable")]
    | typing.Annotated[ByCompareIsWolfBroBulletActivated, pydantic.Tag("ByCompareIsWolfBroBulletActivated")]
    | typing.Annotated[ByCompareItemNum, pydantic.Tag("ByCompareItemNum")]
    | typing.Annotated[ByCompareItemNumber, pydantic.Tag("ByCompareItemNumber")]
    | typing.Annotated[ByCompareMainMissionState, pydantic.Tag("ByCompareMainMissionState")]
    | typing.Annotated[ByCompareMissionBattleWin, pydantic.Tag("ByCompareMissionBattleWin")]
    | typing.Annotated[ByCompareMissionCustomValue, pydantic.Tag("ByCompareMissionCustomValue")]
    | typing.Annotated[ByCompareMusicRhythmSongID, pydantic.Tag("ByCompareMusicRhythmSongID")]
    | typing.Annotated[ByCompareNPCMonsterCheckState, pydantic.Tag("ByCompareNPCMonsterCheckState")]
    | typing.Annotated[ByComparePerformance, pydantic.Tag("ByComparePerformance")]
    | typing.Annotated[ByComparePerformanceResult, pydantic.Tag("ByComparePerformanceResult")]
    | typing.Annotated[ByComparePropAnimState, pydantic.Tag("ByComparePropAnimState")]
    | typing.Annotated[ByComparePropState, pydantic.Tag("ByComparePropState")]
    | typing.Annotated[ByComparePropStateNumber, pydantic.Tag("ByComparePropStateNumber")]
    | typing.Annotated[ByCompareQuestGetReward, pydantic.Tag("ByCompareQuestGetReward")]
    | typing.Annotated[ByCompareQuestProgress, pydantic.Tag("ByCompareQuestProgress")]
    | typing.Annotated[ByCompareRogueMode, pydantic.Tag("ByCompareRogueMode")]
    | typing.Annotated[ByCompareRogueTournLevel, pydantic.Tag("ByCompareRogueTournLevel")]
    | typing.Annotated[ByCompareRogueTournPermanantTalentState, pydantic.Tag("ByCompareRogueTournPermanantTalentState")]
    | typing.Annotated[ByCompareRotatableRegionLoadingState, pydantic.Tag("ByCompareRotatableRegionLoadingState")]
    | typing.Annotated[ByCompareSeriesID, pydantic.Tag("ByCompareSeriesID")]
    | typing.Annotated[ByCompareServerSubMissionState, pydantic.Tag("ByCompareServerSubMissionState")]
    | typing.Annotated[ByCompareStageType, pydantic.Tag("ByCompareStageType")]
    | typing.Annotated[ByCompareStoryLineID, pydantic.Tag("ByCompareStoryLineID")]
    | typing.Annotated[ByCompareSubMissionState, pydantic.Tag("ByCompareSubMissionState")]
    | typing.Annotated[ByCompareTeamLeaderBodySize, pydantic.Tag("ByCompareTeamLeaderBodySize")]
    | typing.Annotated[ByCompareTeamLeaderPath, pydantic.Tag("ByCompareTeamLeaderPath")]
    | typing.Annotated[ByCompareTextJoinValue, pydantic.Tag("ByCompareTextJoinValue")]
    | typing.Annotated[ByCompareVersionFinalMainMission, pydantic.Tag("ByCompareVersionFinalMainMission")]
    | typing.Annotated[ByCompareWaveCount, pydantic.Tag("ByCompareWaveCount")]
    | typing.Annotated[ByContainBehaviorFlag, pydantic.Tag("ByContainBehaviorFlag")]
    | typing.Annotated[ByContainCustomString, pydantic.Tag("ByContainCustomString")]
    | typing.Annotated[ByDeployPuzzleBasePointIsAnswer, pydantic.Tag("ByDeployPuzzleBasePointIsAnswer")]
    | typing.Annotated[ByDistance, pydantic.Tag("ByDistance")]
    | typing.Annotated[ByHasInsertAbilityPending, pydantic.Tag("ByHasInsertAbilityPending")]
    | typing.Annotated[ByHasInsertBattlePerform, pydantic.Tag("ByHasInsertBattlePerform")]
    | typing.Annotated[ByHasUnGottenLevelReward, pydantic.Tag("ByHasUnGottenLevelReward")]
    | typing.Annotated[ByHeroGender, pydantic.Tag("ByHeroGender")]
    | typing.Annotated[ByIfGroupIsOccupied, pydantic.Tag("ByIfGroupIsOccupied")]
    | typing.Annotated[ByInTrackCameraByPathID, pydantic.Tag("ByInTrackCameraByPathID")]
    | typing.Annotated[ByIsActivityInSchedule, pydantic.Tag("ByIsActivityInSchedule")]
    | typing.Annotated[ByIsContainAdventureModifier, pydantic.Tag("ByIsContainAdventureModifier")]
    | typing.Annotated[ByIsContainModifier, pydantic.Tag("ByIsContainModifier")]
    | typing.Annotated[ByIsEraFlipperEntityShow, pydantic.Tag("ByIsEraFlipperEntityShow")]
    | typing.Annotated[ByIsEvolveBuildCountDownItemShow, pydantic.Tag("ByIsEvolveBuildCountDownItemShow")]
    | typing.Annotated[ByIsGenderType, pydantic.Tag("ByIsGenderType")]
    | typing.Annotated[ByIsInDistrict, pydantic.Tag("ByIsInDistrict")]
    | typing.Annotated[ByIsInfiniteBattle, pydantic.Tag("ByIsInfiniteBattle")]
    | typing.Annotated[ByIsRotatableTimeRewindTarget, pydantic.Tag("ByIsRotatableTimeRewindTarget")]
    | typing.Annotated[ByIsShowInActionBar, pydantic.Tag("ByIsShowInActionBar")]
    | typing.Annotated[ByIsSwordTrainingSkillCanLearn, pydantic.Tag("ByIsSwordTrainingSkillCanLearn")]
    | typing.Annotated[ByIsTargetValid, pydantic.Tag("ByIsTargetValid")]
    | typing.Annotated[ByIsTutorialFinish, pydantic.Tag("ByIsTutorialFinish")]
    | typing.Annotated[ByIsUIPageOpen, pydantic.Tag("ByIsUIPageOpen")]
    | typing.Annotated[ByLevelLoseCheck, pydantic.Tag("ByLevelLoseCheck")]
    | typing.Annotated[ByLocalPlayerAvatarID, pydantic.Tag("ByLocalPlayerAvatarID")]
    | typing.Annotated[ByLocalPlayerIsFakeAvatar, pydantic.Tag("ByLocalPlayerIsFakeAvatar")]
    | typing.Annotated[ByLocalPlayerIsHero, pydantic.Tag("ByLocalPlayerIsHero")]
    | typing.Annotated[ByMainMissionFinish, pydantic.Tag("ByMainMissionFinish")]
    | typing.Annotated[ByNot, pydantic.Tag("ByNot")]
    | typing.Annotated[BySimulateSpeedUp, pydantic.Tag("BySimulateSpeedUp")]
    | typing.Annotated[ByTargetListIntersects, pydantic.Tag("ByTargetListIntersects")]
    | typing.Annotated[ByTargetNpcExists, pydantic.Tag("ByTargetNpcExists")]
    | typing.Annotated[ByTimeRewindTargetMotionPause, pydantic.Tag("ByTimeRewindTargetMotionPause")]
    | typing.Annotated[ConvinceByCompareHp, pydantic.Tag("ConvinceByCompareHp")]
    | typing.Annotated[PropPredicateWithEntity, pydantic.Tag("PropPredicateWithEntity")],
    pydantic.Discriminator(get_discriminator),
]
