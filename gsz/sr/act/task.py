from __future__ import annotations

import functools
import typing

from ..excel import Value
from . import model

if typing.TYPE_CHECKING:
    import collections.abc
    import types

    from .. import GameData
    from ..view import TalkSentenceConfig


class Task:
    def __init__(self, game: GameData, task: model.Task):
        self._game: GameData = game
        self._task: model.Task = task

    def is_(self, typ: type | types.UnionType) -> bool:
        return isinstance(self._task, typ)

    @property
    def is_skip(self) -> bool:  # TODO: 慢慢把这些类型效果厘清
        a = (
            model.task.ActiveTemplateVirtualCamera
            | model.task.ActiveVirtualCamera
            | model.task.AddFinishMissionData_ConsumeItem
            | model.task.AddFinishMissionData_SelectConsumeItem
            | model.task.AddFinishMissionData_PlayMessage
            | model.task.AddStreamingSource
            | model.task.AddTrialPlayer
            | model.task.AdvAINavigateTo
            | model.task.AdvCharacterDisableHitBox
            | model.task.AdvClientChangePropState
            | model.task.AdvCreateEntityAsync
            | model.task.AdvCreateGroupEntity
            | model.task.AdvDestroyEntityAsync
            | model.task.AdvDestroyGroupEntity
            | model.task.AdvEnablePropDialogMode
            | model.task.AdvEntityFaceTo
            | model.task.AdvEntityFaceToPoint
            | model.task.AdvEntityStopLookAt
            | model.task.AdventureCameraLookAt
            | model.task.AdventureCameraLookAtSimple
            | model.task.AdventureForbidAttackTriggerBattle
            | model.task.AdventureShowReading
            | model.task.AdvHideMazeBtn
            | model.task.AdvNpcFaceTo
            | model.task.AdvNpcFaceToPlayer
            | model.task.AdvSpecialVisionProtect
            | model.task.AnimSetParameter
        )
        b = model.task.BlockInputController | model.task.ByHeroGender
        c = (
            model.task.CacheUI
            | model.task.CalculateMissionCustomValue
            | model.task.CaptureLocalPlayer
            | model.task.CaptureNPCToCharacter
            | model.task.ChangeDynamicOptionalBlock
            | model.task.ChangeHeartDialModelByScript
            | model.task.ChangeHeroType
            | model.task.ChangePropState
            | model.task.ChangeTeamLeader
            | model.task.ChangeTrackingMission
            | model.task.ChangeTrackVirtualCameraFollowAndAim
            | model.task.CharacterDisableLookAt
            | model.task.CharacterHeadLookAt
            | model.task.CharacterHeadStopLookAt
            | model.task.CharacterNavigateTo
            | model.task.CharacterSteerTo
            | model.task.CharacterStopFreeStyle
            | model.task.CharacterTriggerAnimState
            | model.task.CharacterTriggerFreeStyle
            | model.task.CharacterTriggerFreeStyleGraph
            | model.task.CheckMainMissionFinishedInCurrentVersion
            | model.task.ClearDialogCamera
            | model.task.ClearTalkUI
            | model.task.ClientFinishMission
            | model.task.ClosePage
            | model.task.CollectDataConditions
            | model.task.ConsumeOrigamiItem
            | model.task.ConsumeMissionItem
            | model.task.ConsumeMissionItemPerformance
            | model.task.ConvinceInitialize
            | model.task.ConvinceMoveCurrTurnOption
            | model.task.ConvinceMoveNextTurn
            | model.task.ConvinceMovePrevTurn
            | model.task.ConvinceMoveTurn
            | model.task.ConvincePlayOptionTalk
            | model.task.ConvinceShowToast
            | model.task.ConvinceWaitAllTurnFinish
            | model.task.ConvinceWaitTrickSkill
            | model.task.ConvinceWaitTurnBegin
            | model.task.CreateAirline
            | model.task.CreateLevelAreas
            | model.task.CreateNPC
            | model.task.CreatePhoneOnCharacter
            | model.task.CreateProp
            | model.task.CreateTrialPlayer
        )
        d = (
            model.task.DebateInitialize
            | model.task.DestroyCurvePropGroupPuzzle
            | model.task.DestroyNPC
            | model.task.DestroyProp
            | model.task.DestroyTrialPlayer
        )
        e = (
            model.task.EnableBillboard
            | model.task.EnableNPCMonsterAI
            | model.task.EnablePerformanceMode
            | model.task.EndDialogueEntityInteract
            | model.task.EndPerformance
            | model.task.EndPropInteract
            | model.task.EnterFlipperLightDeviceControl
            | model.task.EnterMap
            | model.task.EnterMapByCondition
        )
        f = (
            model.task.FinishLevelGraph  # 清空选项
            | model.task.FinishPerformanceMission
            | model.task.FinishRogueAeonTalk
            | model.task.ForceSetDialogCamera
        )
        g = model.task.GuessTheSilhouetteResult
        h = (
            model.task.HeliobusSNSQuickPost
            | model.task.HideEntity
            | model.task.HideTopPage
            | model.task.HideWaypointByProp
        )
        l = (  # noqa: E741
            model.task.LensDistortionCurveEffect
            | model.task.LevelAudioState
            | model.task.LevelPerformanceInitialize
            | model.task.LockCurrentTeleportAction
            | model.task.LockPhotoIdentifyHint
            | model.task.LockPlayerControl
            | model.task.LockTeamLeader
        )
        m = model.task.MonsterResearchSubmit | model.task.MoveVirtualCameraOnDollyPath
        n = model.task.NpcPossession | model.task.NpcSetupTrigger | model.task.NpcToPlayerDistanceTrigger
        o = (
            model.task.OpenRaid
            | model.task.OpenTreasureChallenge
            | model.task.OverrideEndTransferType
            | model.task.OverrideFinishActionAutoTransfer
            | model.task.OverridePerformanceEndCrack
        )
        p = (
            model.task.PerformanceEndBlackText
            | model.task.PerformanceEndSeq
            | model.task.PerformanceExtendEndBlack
            | model.task.PhotoGraphAimTarget
            | model.task.PhotoGraphShowIdentifyResult
            | model.task.PhotoGraphWaitIdentifyFinish
            | model.task.PlayerForceWalk
            | model.task.PlayerRemoteControlOtherEntity
            | model.task.PlayerSelectMotionMode
            | model.task.PlayFullScreenTransfer
            | model.task.PlayMazeButtonEffect
            | model.task.PlayNPCBubbleTalk
            | model.task.PlayScreenCrack
            | model.task.PlaySequenceDialogue
            | model.task.PlayTimelinePrefab
            | model.task.PlayVoice
            | model.task.PPFilterStackEffect
            | model.task.PropDestruct
            | model.task.PropEnableCollider
            | model.task.PropMoveTo
            | model.task.PropReqInteract
            | model.task.PropSetupHitBox
            | model.task.PropSetupTrigger
            | model.task.PropSetVisibility
            | model.task.PropStateChangeListenerConfig
            | model.task.PropStateExecute
            | model.task.PropTriggerAnimState
            | model.task.PuzzleSetAnimatorParams
        )
        q = model.task.QuestGetReward
        r = (
            model.task.RadialBlurEffect
            | model.task.RaidSceneTransfer
            | model.task.RandomConfig
            | model.task.ReleaseCacheUI
            | model.task.ReleaseCharacter
            | model.task.RemoveAirline
            | model.task.RemoveBattleEventData
            | model.task.RemoveEffect
            | model.task.RemoveLevelAreas
            | model.task.RemoveMazeBuff
            | model.task.RemoveStreamingSource
            | model.task.RemoveVirtualLineupBindPlane
            | model.task.ReplaceTrialPlayer
            | model.task.ReplaceVirtualTeam
            | model.task.ResetBillboardInfo
            | model.task.ResetMissionAudioState
            | model.task.ResetMissionWayPoint
            | model.task.RogueFinish
            | model.task.RogueShowSelectMainPage
        )
        s = (
            model.task.SaveMessage  # 短信保存到短信箱，打印短信具体见 PlayMessage
            | model.task.SceneGachaListener
            | model.task.SelectMissionItem  # TODO: 提交道具，需要写一写三种后续（提交正确道具后续、提交错误道具对话、取消提交道具对话）
            | model.task.SelectorConfig
            | model.task.SetAdvAchievement
            | model.task.SetAllRogueDoorState
            | model.task.SetAsRogueDialogue
            | model.task.SetAudioEmotionState
            | model.task.SetBillboardInfo
            | model.task.SetCharacterAtlasFaceEmotion
            | model.task.SetCharacterShadowFactor
            | model.task.SetCharacterVisible
            | model.task.SetClockBoyEmotion
            | model.task.SetEffectAnimatorTrigger
            | model.task.SetEntityVisible
            | model.task.SetEntityTalkEnable
            | model.task.SetFloorCustomBool
            | model.task.SetFloorCustomFloat
            | model.task.SetFloorCustomFloatV2
            | model.task.SetFloorCustomString
            | model.task.SetFloorSavedValue
            | model.task.SetLoadingStratageType
            | model.task.SetLocalPlayerDitherAlpha
            | model.task.SetHLODSwitchDelay
            | model.task.SetHudTemplate
            | model.task.SetMissionAudioState
            | model.task.SetMissionCustomValue
            | model.task.SetMissionWayPoint
            | model.task.SetMunicipalEnable
            | model.task.SetNPCMonstersVisible
            | model.task.SetNpcWaypath
            | model.task.SetNpcStatus
            | model.task.SetRogueRoomFinish
            | model.task.SetTraceOrigamiFlag
            | model.task.SetTrackingMission
            | model.task.SetPerformanceResult
            | model.task.SetSpecialVisionOn
            | model.task.SetStageItemState
            | model.task.SetTargetEntityFadeWithAnim
            | model.task.SetTargetUniqueName
            | model.task.SetTextJoinValue
            | model.task.SetVirtualLineupBindPlane
            | model.task.SetWaypointIgnoreLock
            | model.task.ShowActivityPage
            | model.task.ShowEnvBuffDialog
            | model.task.ShowFistClubMissionPage
            | model.task.ShowFuncBtn
            | model.task.ShowGroupChallengeSelectPage
            | model.task.ShowGuideHintWithText
            | model.task.ShowGuideText
            | model.task.ShowHeartDialToast  # 悬浮在大世界的文字，比如梦境里的心理活动
            | model.task.ShowMazeUI
            | model.task.ShowMuseumPage
            | model.task.ShowOfferingClockieUpgradeHint
            | model.task.ShowPerformanceRollingSubtitles
            | model.task.ShowPlayGOSubPackageDialog
            | model.task.ShowRogueTalkBg  # 入口
            | model.task.ShowRogueTalkUI  # 入口
            | model.task.ShowSDFText
            | model.task.ShowShop
            | model.task.ShowSpaceZooMainPage
            | model.task.ShowSubPackage
            | model.task.ShowTalkUI  # 入口
            | model.task.ShowTransitionLoadingUI
            | model.task.ShowTutorialGuide
            | model.task.ShowTutorialUI
            | model.task.ShowUI
            | model.task.ShowWaypointByProp
            | model.task.ShowWorldShop
            | model.task.ShowWorldShop4ThUpgradeHint
            | model.task.SpeedLineEffect
            | model.task.StartDialogueEntityInteract
            | model.task.StartPropInteractMode
            | model.task.StopBlendShapesEmotion
            | model.task.StopPermanentEmotion  # 结束表情，和 TriggerPermanentEmotion 成对
            | model.task.StopRandomMissionTalk
            | model.task.StoryLineReplaceTrialPlayer
            | model.task.SwitchAudioListenerToTarget
            | model.task.SwitchCase
            | model.task.SwitchCharacterAnchor
            | model.task.SwitchCharacterAnchorV2
            | model.task.SwitchPhotoGraphMode
            | model.task.SwitchUIMenuBGM  # 循环播放 BGM
        )
        t = (
            model.task.TeleportToRotatableRegion
            | model.task.ToastPile
            | model.task.TransitEnvProfile
            | model.task.TransitEnvProfileForStory
            | model.task.TriggerBlendShapesEmotion
            | model.task.TriggerCustomString
            | model.task.TriggerCustomStringList
            | model.task.TriggerCustomStringOnDialogEnd
            | model.task.TriggerDialogueEvent  # 怀疑和 WaitDialogueEvent 有什么联动，但是所有文件里的 TriggerDialogueEvent 参数都一样
            | model.task.TriggerDrinkMakerBartendInMainMission
            | model.task.TriggerDrinkMakerBartendInMission
            | model.task.TriggerEffect
            | model.task.TriggerEffectList
            | model.task.TriggerEntityEvent
            | model.task.TriggerEntityEventV2
            | model.task.TriggerGroupEvent
            | model.task.TriggerGroupEventOnDialogEnd
            | model.task.TriggerPermanentEmotion
            | model.task.TriggerRogueDialogue
            | model.task.TriggerSound  # 播放声音
            | model.task.TriggerUINotify
            | model.task.TutorialTaskUnlock
        )
        u = model.task.UnLockPlayerControl | model.task.UpdateTreasureChallengeProgress
        v = model.task.VCameraConfigChange | model.task.VerifyInteractingEntity
        w = (
            model.task.WaitCustomString  # 等待 TriggerCustomString
            | model.task.WaitFrame
            | model.task.WaitFloorCustomValueChange
            | model.task.WaitFloorCustomValueChangeV2
            | model.task.WaitFor
            | model.task.WaitGroupEvent
            | model.task.WaitMissionCustomValueChange
            | model.task.WaitMissionTalkFinish
            | model.task.WaitNewDecalDialogExit
            | model.task.WaitPerformanceEnd  # 出口
            | model.task.WaitPhotoGraphResult
            | model.task.WaitPredicateSucc
            | model.task.WaitPropDestroy
            | model.task.WaitRogueSimpleTalkFinish
            | model.task.WaitSecond  # 等待 TriggerCustomString
            | model.task.WaitSilverWolfCompanionToastExit
            | model.task.WaitStreamingJobFinished
            | model.task.WaitTutorial
            | model.task.WaitUIControllerClose
            | model.task.WaitUIEvent
            | model.task.WaitUINodeOpen
        )
        return isinstance(self._task, a | b | c | d | e | f | g | h | l | m | n | o | p | q | r | s | t | u | v | w)

    @property
    def is_simple(self):
        return isinstance(
            self._task,
            model.task.PlayAeonTalk  # 模拟宇宙中星神出场的对话，会在一开始反复刷新星神名称
            | model.task.PlayAndWaitRogueSimpleTalk
            | model.task.PlayAndWaitSimpleTalk
            | model.task.PlayMissionTalk
            | model.task.PlayMultiVoiceTalk
            | model.task.PlayRogueSimpleTalk
            | model.task.PlaySimpleTalk
            | model.task.WaitSimpleTalkFinish,
        )

    @property
    def is_option(self) -> bool:
        return isinstance(self._task, model.task.PlayOptionTalk | model.task.PlayRogueOptionTalk)

    @staticmethod  # 这个方法应当另外实现一个 class Predicate 挂在下面，但是我懒得写了
    def __predicate_titles(game: GameData, predicate: model.Predicate) -> tuple[str, str]:  # noqa: PLR0911
        match predicate:
            case model.predicate.ByAnd() | model.predicate.ByAny():
                subs = (Task.__predicate_titles(game, pred) for pred in predicate.predicate_list)
                pred = "，且" if isinstance(predicate, model.predicate.ByAnd) else "、或"
                titles = tuple(map(pred.join, zip(*subs, strict=True)))
                assert len(titles) == 2
                return titles
            case model.predicate.ByNot():
                titles = Task.__predicate_titles(game, predicate.predicate)
                return titles[1], titles[0]
            case model.predicate.ByCompareSubMissionState():
                if predicate.sub_mission_id is None:
                    return ("", "")
                sub_mission = game.sub_mission(predicate.sub_mission_id)
                target = (
                    sub_mission and (sub_mission.target or sub_mission.description) or str(predicate.sub_mission_id)
                )
                match predicate.sub_mission_state:
                    case model.predicate.MissionState.Started:
                        success_state, failure_state = "进行中", "未开始"
                    case model.predicate.MissionState.Finish:
                        success_state, failure_state = "已完成", "未完成"
                    case None:
                        success_state, failure_state = "", ""
                return (f"「{target}」{success_state}", f"「{target}」{failure_state}")
            case model.predicate.ByHeroGender():
                match predicate.gender:
                    case model.predicate.Gender.Man:
                        return ("男开拓者", "女开拓者")
                    case model.predicate.Gender.Woman:
                        return ("女开拓者", "男开拓者")
            case _:
                return (f"<!-- {predicate} -->", f"<!-- {predicate} -->")

    def predicate_titles(self) -> tuple[str, str]:
        if not isinstance(self._task, model.task.PredicateTaskList):
            return ("", "")
        return self.__predicate_titles(self._game, self._task.predicate)

    @property
    def trigger_custom_string(self) -> str:
        if isinstance(self._task, model.task.TriggerCustomString | model.task.TriggerCustomStringOnDialogEnd):
            return "" if isinstance(self._task.custom_string, model.Custom) else self._task.custom_string.value
        return ""

    @property
    def wait_custom_string(self) -> str:
        if not isinstance(self._task, model.task.WaitCustomString):
            return ""
        if not isinstance(self._task.custom_string, Value):
            return ""
        return self._task.custom_string.value

    @functools.cached_property
    def __talks(self) -> list[TalkSentenceConfig]:
        if isinstance(self._task, model.task.PlayMultiVoiceTalk):
            talk = self._game.talk_sentence_config(self._task.talk_sentence_id)
            assert talk is not None
            return [talk]
        if isinstance(
            self._task,
            model.task.PlayAeonTalk
            | model.task.PlayAndWaitRogueSimpleTalk
            | model.task.PlayAndWaitSimpleTalk
            | model.task.PlayMissionTalk
            | model.task.PlayMultiVoiceTalk
            | model.task.PlayRogueSimpleTalk
            | model.task.PlaySimpleTalk,
        ):
            talk_sentences = (
                self._game.talk_sentence_config(talk.talk_sentence_id)
                for talk in self._task.simple_talk_list
                if talk.talk_sentence_id is not None
            )
            return list(filter(None, talk_sentences))
        return []

    def talks(self) -> collections.abc.Iterable[TalkSentenceConfig]:
        from ..view.talk import TalkSentenceConfig

        return (TalkSentenceConfig(self._game, talk._excel) for talk in self.__talks)  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def __backgrounds(self) -> list[str | None]:
        if not isinstance(self._task, model.task.PlayAndWaitSimpleTalk | model.task.PlaySimpleTalk):
            return []
        if self._task.backgrounds is None:
            return []
        backgrounds: list[str | None] = []
        for background in self._task.backgrounds:
            if background.image_path is None and background.cg_id is None:
                backgrounds.append(None)
            elif background.image_path is not None:
                backgrounds.append(background.image_path)
            elif background.cg_id is not None:
                cg = self._game.loop_cg_config(background.cg_id)
                backgrounds.append("" if cg is None else cg.path)
        return backgrounds

    def backgrounds(self) -> collections.abc.Iterable[str | None]:
        yield from self.__backgrounds

    @functools.cached_property
    def __options(self) -> collections.abc.Sequence[model.talk.OptionTalk]:
        if isinstance(self._task, model.task.PlayRogueOptionTalk):
            return self._task.option_list
        if isinstance(self._task, model.task.PlayOptionTalk):
            return self._task.option_list
        return []

    def options(self) -> collections.abc.Iterable[model.talk.OptionTalk]:
        return (option for option in self.__options)
