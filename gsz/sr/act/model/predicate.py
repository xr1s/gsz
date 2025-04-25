import enum
import typing

import pydantic

from ...excel import Path, Text, Value, item
from . import mission, target
from .base import Custom, Dynamic, FixedValue, Model, get_discriminator


class CompareType(enum.Enum):
    Equal = "Equal"
    Greater = "Greater"
    GreaterEqual = "GreaterEqual"
    Less = "Less"
    LessEqual = "LessEqual"
    NotEqual = "NotEqual"


class MissionState(enum.Enum):
    Started = "Started"
    Finish = "Finish"


class AdvByCompareDimensionID(Model):
    compare_type: CompareType
    compare_value: int | None = None


class AdvByEntitiesExist(Model):
    target_type: target.Target


class AdvByEntityExist(Model):
    target_type: target.Target


class AdvByFastDeliverHasMultiRoute(Model):
    target: target.Target


class AdvByPlayerInVisionZone(Model):
    zone_tags: list[str]


class AdventureByCompareMP(Model):
    compare_type: CompareType


class AdventureByPropInPosition(Model):
    target_group_id: int
    target_group_prop_id: int
    source_is_owner: typing.Literal[True]
    ignore_y_asix: typing.Literal[True]
    range: float
    target_type: target.Target


class AdventureByPropShowInfoId(Model):
    target_type: target.Target


class AdventureIsTriggerBattleByNpcMonster(Model):
    pass


class ByAdvCharacterLogicState(Model):
    target_type: target.Target
    type: typing.Literal["OnHit"]
    inverse: bool = False


class ByAnd(Model):
    predicate_list: list["Predicate"]
    inverse: bool = False


class ByAny(Model):
    predicate_list: list["Predicate"]


class ByAnyNpcMonsterInRange(Model):
    consider_obstacle: typing.Literal[True]
    range: float
    angle_limit: int


class ByCheckAdditionalConditions(Model):
    check_for_win: bool = False


class ByCheckColonyTrace(Model):
    colony_id: FixedValue[int]
    inverse: bool = False


class ByCheckDarkTeamDestroy(Model):
    for_wave_end: typing.Literal[True]


class ByCheckFloorCustomBool(Model):
    name: Value[str]
    inverse: bool = False


class ByCheckRogueExploreWin(Model):
    pass


class ByCheckTimelineEntityState(Model):
    target: target.Target
    state_name: Value[str]


class ByCheckTrialCharacterDie(Model):
    pass


class ByCheckLineupHeroAvatarID(Model):
    pass


class ByCompareCarryMazebuff(Model):
    target_type: target.Target
    buff_id: int


class ByCompareCurrentTeammemberCount(Model):
    equation_type: CompareType
    target_count: int


class ByCompareCustomString(Model):
    left_value: Custom
    right_value: Value[str]
    compare_type: CompareType


class ByCompareDynamicValue(Model):
    target_type: target.Target
    dynamic_key: Value[str]
    context_scope: typing.Literal["TargetEntity"]
    compare_type: CompareType
    complare_value: FixedValue[int]


class ByCompareEventMissionState(Model):
    event_mission_id: int
    sub_mission_state: MissionState


class ByCompareFloorCustomFloat(Model):
    name: Value[str] | Custom
    compare_type: CompareType
    compare_value: FixedValue[int]


class ByCompareFloorCustomFloatV2(Model):
    name: Value[str]
    compare_type: CompareType
    compare_value: FixedValue[int]


class ByCompareFloorCustomString(Model):
    name: Value[str]
    compare_type: CompareType
    compare_value: Value[str]
    inverse: bool = False


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
    name: str
    value: FixedValue[float]
    compare_type: CompareType


class ByCompareGraphDynamicString(Model):
    name: str
    value: Value[str]


class ByCompareGroupMonsterNumByState(Model):
    pass


class ByCompareGroupState(Model):
    equation_type: CompareType
    value: int | None = None


class ByCompareHeartDialTracingNPC(Model):
    inverse: bool = False


class ByCompareHPRatio(Model):
    target_type: target.Target
    compare_type: CompareType
    compare_value: FixedValue[float]


class ByCompareIsBookAvailable(Model):
    book_series_id: int
    book_id: int
    inverse: bool = False


class ByCompareIsWolfBroBulletActivated(Model):
    pass


class ByCompareItemNum(Model):
    item_pair: list[item.Pair]
    inverse: bool = False


class ByCompareItemNumber(Model):
    item_id: FixedValue[int]
    number: FixedValue[int]
    compare_type: CompareType


class ByCompareMainMissionState(Model):
    main_mission_id: int
    main_mission_state: MissionState | None = None
    all_story_line: bool = False
    inverse: bool = False


class ByCompareMissionBattleWin(Model):
    event_id: int


class ByCompareMissionCustomValue(Model):
    main_mission_id: int
    mission_custom_value: mission.MissionCustomValue
    equation_type: CompareType | None = None
    show_compare_value: bool = False
    target_value: int | None = None
    mission_custom_value_compare: mission.MissionCustomValue | None = None


class ByCompareMusicRhythmSongID(Model):
    song_id: int
    inverse: bool = False


class ByCompareNPCMonsterCheckState(Model):
    group_id: FixedValue[int]
    group_monster_id: FixedValue[int]
    check_state: typing.Literal["Dead"]


class ByComparePerformance(Model):
    performance_id: int
    performance_id_ds: typing.Annotated[Value[typing.Literal["E"]] | None, pydantic.Field(alias="PerformanceID_DS")] = (
        None
    )
    inverse: bool = False


class ByComparePerformanceResult(Model):
    compare_type: CompareType
    compare_value: int


class ByComparePropAnimState(Model):
    class State(enum.Enum):
        Closed = "Closed"
        Opened01 = "Opened01"
        PlayerCrouch = "PlayerCrouch"
        TriggerSelectLoop = "TriggerSelectLoop"

    state: State
    target_type: target.Target


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
    group_id: FixedValue[int] | Dynamic
    prop_id_list: list[FixedValue[int] | Dynamic]
    state: typing.Literal["Open"]
    compare_type: CompareType
    compare_value: int


class ByCompareQuestGetReward(Model):
    quest_id: FixedValue[int]
    inverse: bool = False


class ByCompareQuestProgress(Model):
    quest_id: FixedValue[int]
    progress: FixedValue[int]
    equation_type: CompareType


class ByCompareRogueMode(Model):
    rogue_mode: typing.Literal["RogueMode"]


class ByCompareRogueTournPermanantTalentState(Model):
    pass


class ByCompareRotatableRegionLoadingState(Model):
    region_index: Dynamic
    compare_state: typing.Literal["Ready"]


class ByCompareSeriesID(Model):
    pass


class ByCompareServerSubMissionState(Model):
    pass


class ByCompareStageType(Model):
    current_stage_type: typing.Literal["AetherDivide", "EvolveBuildActivity"]


class ByCompareStoryLineID(Model):
    target_story_line_id: int | None = None


class ByCompareSubMissionState(Model):
    sub_mission_id: int | None = None
    sub_mission_state: MissionState | None = None
    all_story_line: bool = False
    inverse: bool = False


class ByCompareTeamLeaderBodySize(Model):
    body_size: typing.Literal["Boy", "Girl", "Kid"]


class ByCompareTeamLeaderPath(Model):
    path_type: Path


class ByCompareTextJoinValue(Model):
    text_join_id: int
    value: int


class ByCompareVersionFinalMainMission(Model):
    main_mission_id: int


class ByCompareWaveCount(Model):
    compare_type: CompareType
    compoare_with_max: typing.Literal[True]


class ByContainBehaviorFlag(Model):
    target_type: target.Target


class ByContainCustomString(Model):
    key: Text


class ByDeployPuzzleBasePointIsAnswer(Model):
    target_type: target.Target


class ByDieAnimFinished(Model):
    team_type_mask: typing.Literal["TeamDark"]
    entity_type_mask: typing.Literal["Mask_TeamCharacters"]


class ByDistance(Model):
    from_: target.Target
    to: target.Target
    compare_type: CompareType
    compare_value: FixedValue[int]
    ignore_radius: bool = True


class ByHasInsertAbilityPending(Model):
    pass


class ByHasInsertBattlePerform(Model):
    inverse: bool = False


class ByHasUnGottenLevelReward(Model):
    pass


class Gender(enum.Enum):
    Man = "GENDER_MAN"
    Woman = "GENDER_WOMAN"


class ByHeroGender(Model):
    gender: Gender


class ByIfGroupIsOccupied(Model):
    group_id: int


class ByInTrackCameraByPathID(Model):
    use_owner_group: typing.Literal[True]
    path_id: FixedValue[typing.Literal[1]]
    detect_range: Dynamic


class ByIsActivityInSchedule(Model):
    activity_panel_id: int


class ByIsContainAdventureModifier(Model):
    target_type: target.Target
    modifier_name: str


class ByIsContainModifier(Model):
    target_type: target.Target
    modifier_name: Value[str]


class ByIsEraFlipperEntityShow(Model):
    inverse: bool = False


class ByIsEvolveBuildCountDownItemShow(Model):
    pass


class ByIsGenderType(Model):
    gender: Gender


class ByIsInDistrict(Model):
    district_type: target.Target
    target_type: target.Target


class ByIsInfiniteBattle(Model):
    pass


class ByIsRotatableTimeRewindTarget(Model):
    pass


class ByIsShowInActionBar(Model):
    character_id: int


class ByIsSwordTrainingSkillCanLearn(Model):
    skill_id: int


class ByIsTargetValid(Model):
    target_type: target.Target


class ByIsTutorialFinish(Model):
    tutorial_id: int


class ByIsUIPageOpen(Model):
    page_name: typing.Literal["RogueSelectMainPage"]


class ByLevelLoseCheck(Model):
    pass


class ByLocalPlayerAvatarID(Model):
    avatar_ids: typing.Annotated[list[int], pydantic.Field(alias="AvatarIDs")]


class ByLocalPlayerIsFakeAvatar(Model):
    inverse: bool = False


class ByLocalPlayerIsHero(Model):
    pass


class ByMainMissionFinish(Model):
    main_mission_id: int
    inverse: bool = False


class ByNot(Model):
    predicate: "Predicate"


class BySimulateSpeedUp(Model):
    pass


class ByTargetListIntersects(Model):
    first_target_type: target.Target
    second_target_type: target.Target


class ByTargetNpcExists(Model):
    group_id: int
    group_npc_id: int


class ByTimeRewindTargetMotionPause(Model):
    target: target.Target


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
    | typing.Annotated[ByCheckAdditionalConditions, pydantic.Tag("ByCheckAdditionalConditions")]
    | typing.Annotated[ByCheckColonyTrace, pydantic.Tag("ByCheckColonyTrace")]
    | typing.Annotated[ByCheckDarkTeamDestroy, pydantic.Tag("ByCheckDarkTeamDestroy")]
    | typing.Annotated[ByCheckFloorCustomBool, pydantic.Tag("ByCheckFloorCustomBool")]
    | typing.Annotated[ByCheckRogueExploreWin, pydantic.Tag("ByCheckRogueExploreWin")]
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
    | typing.Annotated[ByDieAnimFinished, pydantic.Tag("ByDieAnimFinished")]
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
