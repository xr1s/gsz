import enum
import typing

import pydantic

from .base import Model, get_discriminator


class AdvByEntitiesExist(Model):
    pass


class AdvByEntityExist(Model):
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


class ByAnd(Model):
    pass


class ByAny(Model):
    pass


class ByAnyNpcMonsterInRange(Model):
    pass


class ByCheckColonyTrace(Model):
    pass


class ByCheckFloorCustomBool(Model):
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


class ByCompareFloorCustomFloat(Model):
    pass


class ByCompareFloorCustomString(Model):
    pass


class ByCompareFloorSavedValue(Model):
    pass


class ByCompareGraphDynamicFloat(Model):
    pass


class ByCompareGraphDynamicString(Model):
    pass


class ByCompareGroupMonsterNumByState(Model):
    pass


class ByCompareGroupState(Model):
    pass


class ByCompareHeartDialTracingNPC(Model):
    pass


class ByCompareIsBookAvailable(Model):
    pass


class ByCompareIsWolfBroBulletActivated(Model):
    pass


class ByCompareItemNum(Model):
    pass


class ByCompareItemNumber(Model):
    pass


class ByCompareMainMissionState(Model):
    pass


class ByCompareMissionBattleWin(Model):
    pass


class MissionCustomValue(Model):
    is_local: typing.Annotated[bool, pydantic.Field(alias="isLocal")] = False
    is_range: typing.Annotated[bool, pydantic.Field(alias="isRange")] = False
    valid_value_param_list: list[int]


class EquationType(enum.Enum):
    Equal = "Equal"
    Greater = "Greater"
    GreaterEqual = "GreaterEqual"
    Less = "Less"
    LessEqual = "LessEqual"
    NotEqual = "NotEqual"


class ByCompareMissionCustomValue(Model):
    main_mission_id: int
    mission_custom_value: MissionCustomValue
    equation_type: EquationType | None


class ByCompareMusicRhythmSongID(Model):
    pass


class ByCompareNPCMonsterCheckState(Model):
    pass


class ByComparePerformance(Model):
    pass


class ByComparePerformanceResult(Model):
    pass


class ByComparePropAnimState(Model):
    pass


class ByComparePropState(Model):
    pass


class ByComparePropStateNumber(Model):
    pass


class ByCompareQuestProgress(Model):
    pass


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


class ByCompareStageType(Model):
    pass


class ByCompareStoryLineID(Model):
    pass


class ByCompareSubMissionState(Model):
    pass


class ByCompareTeamLeaderPath(Model):
    pass


class ByCompareTextJoinValue(Model):
    pass


class ByCompareVersionFinalMainMission(Model):
    pass


class ByCompareWaveCount(Model):
    pass


class ByContainCustomString(Model):
    pass


class ByDeployPuzzleBasePointIsAnswer(Model):
    pass


class ByDistance(Model):
    pass


class ByHasInsertAbilityPending(Model):
    pass


class ByHasUnGottenLevelReward(Model):
    pass


class ByHeroGender(Model):
    pass


class ByIsContainAdventureModifier(Model):
    pass


class ByIsContainModifier(Model):
    pass


class ByIsEvolveBuildCountDownItemShow(Model):
    pass


class ByIsGenderType(Model):
    pass


class ByIsInfiniteBattle(Model):
    pass


class ByIsShowInActionBar(Model):
    pass


class ByIsSwordTrainingSkillCanLearn(Model):
    pass


class ByIsTargetValid(Model):
    pass


class ByIsUIPageOpen(Model):
    pass


class ByLocalPlayerAvatarID(Model):
    pass


class ByLocalPlayerIsFakeAvatar(Model):
    pass


class ByMainMissionFinish(Model):
    pass


class ByNot(Model):
    pass


class BySimulateSpeedUp(Model):
    pass


class ByTargetListIntersects(Model):
    pass


class ByTargetNpcExists(Model):
    pass


class ConvinceByCompareHp(Model):
    pass


class PropPredicateWithEntity(Model):
    pass


Predicate = typing.Annotated[
    typing.Annotated[AdvByEntitiesExist, pydantic.Tag("AdvByEntitiesExist")]
    | typing.Annotated[AdvByEntityExist, pydantic.Tag("AdvByEntityExist")]
    | typing.Annotated[AdvByPlayerInVisionZone, pydantic.Tag("AdvByPlayerInVisionZone")]
    | typing.Annotated[AdventureByCompareMP, pydantic.Tag("AdventureByCompareMP")]
    | typing.Annotated[AdventureByPropInPosition, pydantic.Tag("AdventureByPropInPosition")]
    | typing.Annotated[AdventureByPropShowInfoId, pydantic.Tag("AdventureByPropShowInfoId")]
    | typing.Annotated[AdventureIsTriggerBattleByNpcMonster, pydantic.Tag("AdventureIsTriggerBattleByNpcMonster")]
    | typing.Annotated[ByAnd, pydantic.Tag("ByAnd")]
    | typing.Annotated[ByAny, pydantic.Tag("ByAny")]
    | typing.Annotated[ByAnyNpcMonsterInRange, pydantic.Tag("ByAnyNpcMonsterInRange")]
    | typing.Annotated[ByCheckColonyTrace, pydantic.Tag("ByCheckColonyTrace")]
    | typing.Annotated[ByCheckFloorCustomBool, pydantic.Tag("ByCheckFloorCustomBool")]
    | typing.Annotated[ByCheckLineupHeroAvatarID, pydantic.Tag("ByCheckLineupHeroAvatarID")]
    | typing.Annotated[ByCompareCarryMazebuff, pydantic.Tag("ByCompareCarryMazebuff")]
    | typing.Annotated[ByCompareCurrentTeammemberCount, pydantic.Tag("ByCompareCurrentTeammemberCount")]
    | typing.Annotated[ByCompareCustomString, pydantic.Tag("ByCompareCustomString")]
    | typing.Annotated[ByCompareDynamicValue, pydantic.Tag("ByCompareDynamicValue")]
    | typing.Annotated[ByCompareEventMissionState, pydantic.Tag("ByCompareEventMissionState")]
    | typing.Annotated[ByCompareFloorCustomFloat, pydantic.Tag("ByCompareFloorCustomFloat")]
    | typing.Annotated[ByCompareFloorCustomString, pydantic.Tag("ByCompareFloorCustomString")]
    | typing.Annotated[ByCompareFloorSavedValue, pydantic.Tag("ByCompareFloorSavedValue")]
    | typing.Annotated[ByCompareGraphDynamicFloat, pydantic.Tag("ByCompareGraphDynamicFloat")]
    | typing.Annotated[ByCompareGraphDynamicString, pydantic.Tag("ByCompareGraphDynamicString")]
    | typing.Annotated[ByCompareGroupMonsterNumByState, pydantic.Tag("ByCompareGroupMonsterNumByState")]
    | typing.Annotated[ByCompareGroupState, pydantic.Tag("ByCompareGroupState")]
    | typing.Annotated[ByCompareHeartDialTracingNPC, pydantic.Tag("ByCompareHeartDialTracingNPC")]
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
    | typing.Annotated[ByCompareQuestProgress, pydantic.Tag("ByCompareQuestProgress")]
    | typing.Annotated[ByCompareRogueMode, pydantic.Tag("ByCompareRogueMode")]
    | typing.Annotated[ByCompareRogueTournLevel, pydantic.Tag("ByCompareRogueTournLevel")]
    | typing.Annotated[ByCompareRogueTournPermanantTalentState, pydantic.Tag("ByCompareRogueTournPermanantTalentState")]
    | typing.Annotated[ByCompareRotatableRegionLoadingState, pydantic.Tag("ByCompareRotatableRegionLoadingState")]
    | typing.Annotated[ByCompareSeriesID, pydantic.Tag("ByCompareSeriesID")]
    | typing.Annotated[ByCompareStageType, pydantic.Tag("ByCompareStageType")]
    | typing.Annotated[ByCompareStoryLineID, pydantic.Tag("ByCompareStoryLineID")]
    | typing.Annotated[ByCompareSubMissionState, pydantic.Tag("ByCompareSubMissionState")]
    | typing.Annotated[ByCompareTeamLeaderPath, pydantic.Tag("ByCompareTeamLeaderPath")]
    | typing.Annotated[ByCompareTextJoinValue, pydantic.Tag("ByCompareTextJoinValue")]
    | typing.Annotated[ByCompareVersionFinalMainMission, pydantic.Tag("ByCompareVersionFinalMainMission")]
    | typing.Annotated[ByCompareWaveCount, pydantic.Tag("ByCompareWaveCount")]
    | typing.Annotated[ByContainCustomString, pydantic.Tag("ByContainCustomString")]
    | typing.Annotated[ByDeployPuzzleBasePointIsAnswer, pydantic.Tag("ByDeployPuzzleBasePointIsAnswer")]
    | typing.Annotated[ByDistance, pydantic.Tag("ByDistance")]
    | typing.Annotated[ByHasInsertAbilityPending, pydantic.Tag("ByHasInsertAbilityPending")]
    | typing.Annotated[ByHasUnGottenLevelReward, pydantic.Tag("ByHasUnGottenLevelReward")]
    | typing.Annotated[ByHeroGender, pydantic.Tag("ByHeroGender")]
    | typing.Annotated[ByIsContainAdventureModifier, pydantic.Tag("ByIsContainAdventureModifier")]
    | typing.Annotated[ByIsContainModifier, pydantic.Tag("ByIsContainModifier")]
    | typing.Annotated[ByIsEvolveBuildCountDownItemShow, pydantic.Tag("ByIsEvolveBuildCountDownItemShow")]
    | typing.Annotated[ByIsGenderType, pydantic.Tag("ByIsGenderType")]
    | typing.Annotated[ByIsInfiniteBattle, pydantic.Tag("ByIsInfiniteBattle")]
    | typing.Annotated[ByIsShowInActionBar, pydantic.Tag("ByIsShowInActionBar")]
    | typing.Annotated[ByIsSwordTrainingSkillCanLearn, pydantic.Tag("ByIsSwordTrainingSkillCanLearn")]
    | typing.Annotated[ByIsTargetValid, pydantic.Tag("ByIsTargetValid")]
    | typing.Annotated[ByIsUIPageOpen, pydantic.Tag("ByIsUIPageOpen")]
    | typing.Annotated[ByLocalPlayerAvatarID, pydantic.Tag("ByLocalPlayerAvatarID")]
    | typing.Annotated[ByLocalPlayerIsFakeAvatar, pydantic.Tag("ByLocalPlayerIsFakeAvatar")]
    | typing.Annotated[ByMainMissionFinish, pydantic.Tag("ByMainMissionFinish")]
    | typing.Annotated[ByNot, pydantic.Tag("ByNot")]
    | typing.Annotated[BySimulateSpeedUp, pydantic.Tag("BySimulateSpeedUp")]
    | typing.Annotated[ByTargetListIntersects, pydantic.Tag("ByTargetListIntersects")]
    | typing.Annotated[ByTargetNpcExists, pydantic.Tag("ByTargetNpcExists")]
    | typing.Annotated[ConvinceByCompareHp, pydantic.Tag("ConvinceByCompareHp")]
    | typing.Annotated[PropPredicateWithEntity, pydantic.Tag("PropPredicateWithEntity")],
    pydantic.Discriminator(get_discriminator),
]
