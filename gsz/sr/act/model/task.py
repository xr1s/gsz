import enum
import pathlib
import sys
import typing

import pydantic

from ... import excel
from ...excel import Text, Value
from . import camera, input, mission, performance, predicate, select_mission_item, talk, target, value
from .base import Axis, BaseModel, Custom, Dynamic, Empty, FixedValue, Model, get_discriminator
from .target import Target

sys.setrecursionlimit(2500)


class ActiveTemplateVirtualCamera(Model):
    template_name: Value[str]
    follow_offset: float | None = None
    camera_rotation: Axis | None = None
    camera_rotation_offset: float | None = None
    is_active: bool = True
    follow_target_group_id: int
    follow_target_entity_id: int
    look_at_target_group_id: int
    look_at_target_entity_id: int


class ActiveVirtualCamera(Model):
    class DynamicParams(BaseModel):
        orbital_transposer_bias: bool = False

    area_name: str | None = None
    anchor_name: str | None = None
    level_area_camera_key: Value[str] | Custom | None = None
    is_entry_point_camera: bool = False
    is_active: bool = False
    follow_target_anchor_name: str | None = None
    follow_target_unique_name: str | None = None
    follow_target_attach_point: camera.AttachPoint | None = None
    look_at_target_anchor_name: str | None = None
    look_at_target_unique_name: str | None = None
    look_at_target_attach_point: camera.AttachPoint | None = None
    select_follow_target_type: typing.Literal["Target"] | None = None
    select_look_at_target_type: typing.Literal["Target"] | None = None
    look_at_target: target.Target | None = None
    wait_blend_finish: bool = False
    blend_config: camera.BlendConfig | None = None
    override_blend_curve_name: Value[str] | None = None
    disable_protect_when_blending: bool = False
    v_camera_dither_npc_on: typing.Annotated[bool, pydantic.Field(alias="VCameraDitherNPCOn")] = False
    v_camera_dither_max_distance: int | None = None
    dynamic_params: DynamicParams | None = None
    immediately_refresh: bool = False
    keep_main_camera_rotation: bool = False
    task_enabled: bool = True


class ActiveVirtualCamera_PerformanceTransition(Model):
    area_name: str
    anchor_name: str
    is_active: bool = True


class AddFinishMissionData_ConsumeItem(Model):
    submission_id: int
    is_show_consume_finish_tips: bool = False
    only_performance: bool = False
    desc: Text | None = None
    is_auto_consume: bool = False
    simple_talk: dict[None, None]
    on_submit_confirm: list["Task"] | None = None
    on_submit_cancel: list["Task"] | None = None


class AddFinishMissionData_SelectConsumeItem(Model):
    submission_id: int
    only_performance: bool = True
    item_id_list: list[int]
    item_hidden_id_list: list[None]
    item_invisible_id_list: list[None]
    item_select: list[select_mission_item.ItemSelect]
    slot_num: int
    simple_talk: select_mission_item.SimpleTalk
    on_submit_fail: list["Task"] | None = None
    on_submit_cancel: list["Task"] | None = None


class AddFinishMissionData_PlayMessage(Model):
    submission_id: int
    message_section_id: int
    show_notice: bool = True


class AddStreamingSource(Model):
    class StreamingSource(BaseModel):
        center_name: str
        area_name: str
        anchor_name: str

    streaming_source: StreamingSource


class AddTrialPlayer(Model):
    pass


class AdvAINavigateTo(Model):
    class Mode(enum.Enum):
        Anchor = "Anchor"
        NavigateToEntity = "NavigateToEntity"

    class MotionFlag(enum.Enum):
        FastRun = "FastRun"
        Run = "Run"
        Walk = "Walk"

    target_type: target.Target
    mode: Mode | None = None
    motion_flag: MotionFlag
    navigate_target: target.Target | None = None
    level_area_key: Custom | None = None
    navigate_position: Axis | None = None
    wait_finish: bool = False


class AdvCharacterDisableHitBox(Model):
    target_type: target.Target
    affect_main_collider: bool = False
    enable: bool = True


class AdvClientChangePropState(Model):
    target_type: target.Target
    from_state: predicate.PropState | None = None
    to_state: predicate.PropState | None = None
    can_change_server_prop: bool = False


class AdvCreateEntityAsync(Model):
    instance_id_list: list[int]
    advanced_spawn_list: list[int]


class AdvCreateGroupEntity(Model):
    instance_id_list: list[int]
    task_enabled: bool = True


class AdvCreateGroupEntityV2(Model):
    instance_id_list: list[int]


class AdvDestroyEntityAsync(Model):
    need_disappear: bool = False
    instance_id_list: list[int]
    advanced_spawn_list: list[None] | None = None


class AdvDestroyGroupEntity(Model):
    instance_id_list: list[int]


class AdvEnablePropDialogMode(Model):
    is_use_program_rotate: bool = False
    rotate_speed: int | None = None
    enable: bool = True
    player_face_to_prop: bool = True
    enable_prop_camera: bool = True
    lock_player_control: bool = False
    is_immediately_succ: bool = False
    target_type: target.Target


class AdvEntityFaceTo(Model):
    source_type: target.Target
    target_type: target.Target | None = None
    enable_steer: bool = False
    look_at_point: camera.AttachPoint | None = None
    steer_immediately: bool = False
    enable_look_at: bool = True
    finish_immediately: bool = True
    wait_finish_mode: camera.WaitFinishMode | None = None
    force_to_stand_by: bool = False
    turn_back_on_graph_end: bool = True
    task_enabled: bool = True


class AdvEntityFaceToPoint(Model):
    source_type: target.Target
    group_id: typing.Annotated[int, pydantic.Field(alias="GroupId")]
    point_id: int


class AdvEntityStopLookAt(Model):
    source_type: target.Target
    target_type: target.Target | None = None
    stop_immediately: bool = False
    task_enabled: bool = True


class AdventureCameraLookAt(Model):
    look_at_group_id: FixedValue[int] | None = None
    look_at_id: FixedValue[int] | None = None
    reset: bool = False
    look_at_target_area_name: Value[str] | None = None
    look_at_target_anchor_name: Value[str] | None = None
    player_turn_to: bool = False
    axis_offset: Axis | None = None
    look_at_transition_duration: float
    look_at_transition_curve_path: str
    lock_camera_input: bool = False
    unlock_camera_after_recover: bool = False
    look_at_duration: int | None = None
    max_angle: int
    extra_freelook_3rd_config: camera.Freelook3rdConfig | None = None
    follow_look_at_target: bool = True
    screen_range: camera.ScreenRange | None = None


class AdventureCameraLookAtSimple(Model):
    look_at_group_id: FixedValue[int] | None = None
    look_at_id: FixedValue[int] | None = None
    reset: bool = False
    look_at_target: target.Target | None = None
    look_at_target_area_name: Value[str] | None = None
    look_at_target_anchor_name: Value[str] | None = None
    cut_in: bool = False
    cut_out: bool = False
    look_at_transition_duration: typing.Literal[1, 2] | None = None
    look_at_transition_curve_path: str | None = None
    lock_camera_input: bool = False
    unlock_camera_after_recover: bool = False
    look_at_duration: int | None = None
    look_at_recover_duration: float | None = None
    look_at_recover_curve_path: str | None = None
    enable_override_look_at_offset: bool = False
    override_look_at_offset: Axis | None = None
    screen_range: camera.ScreenRange | None = None
    task_enabled: bool = True


class AdventureForbidAttackTriggerBattle(Model):
    is_forbid: bool = False


class AdventureShowReading(Model):
    book_id: FixedValue[int]


class AdvHideMazeBtn(Model):
    skill_type: typing.Literal["MazeSkill"] | None = None
    is_hide: bool = True


class AdvNpcFaceTo(Model):
    group_id: int | None = None
    group_npc_id: int | None = None
    area_name: str
    anchor_name: str
    finish_immadiate: bool = False


class AdvNpcFaceToPlayer(Model):
    from_dialog: bool = True
    group_id: int | None = None
    group_npc_id: int | None = None
    duration: int | None = None
    player_in_group_id: int | None = None
    player_in_group_npc_id: int | None = None
    target_npc_type: target.Target | None = None
    target_player_type: target.Target | None = None
    try_face_to_face: bool = True
    only_player_face_to_npc: bool = False
    npc_look_at_player: bool = True
    player_look_at_npc: bool = True
    stop_look_at_on_graph_end: bool = True
    turn_back_on_graph_end: bool = True
    steer_immediately: bool = False
    finish_immadiate: bool = False
    wait_finish_mode: camera.WaitFinishMode | None = None
    force_to_stand_by: bool = True
    task_enabled: bool = True


class AdvSetAIFollow(Model):
    fetch_target: typing.Literal[True]
    target_type: target.Target
    fetch_follow_target: typing.Literal[True]
    follow_target_type: target.Target
    prefer_slot_i_ds: list[int]


class AdvSpecialVisionProtect(Model):
    pass


class AnimSetParameter(Model):
    target_type: target.Target | None = None
    animator_path: str | None = None
    parameter_name: str
    parameter_type: typing.Literal["Bool", "Int", "Trigger"]
    value: FixedValue[int] | None = None


class BattlePerformInit(Model):
    area_prefab_path: str
    capture_entity: bool = False
    capture_team_light_list: list[performance.CaptureTeam]
    capture_team_dark_list: list[performance.CaptureTeam]


class BattlePerformTimeline(Model):
    timeline_path: pathlib.Path


class BattlePlayVideo(Model):
    video_id: int
    can_skip: bool = False
    mute_bgm_with_fade_out: bool = False
    start_black: excel.performance.BlackType


class BlockInputController(Model):
    enable: bool = False
    action_name_list: list[input.ActionName]
    task_enabled: bool = True


class ByHeroGender(Model):
    gender: predicate.Gender


class CacheUI(Model):
    prefab_paths: list[str]


class CalculateMissionCustomValue(Model):
    class Value(BaseModel):
        type: typing.Literal["CustomValue"] | None = None
        direct_value: int | None = None
        main_mission_id: int | None = None
        mission_custom_value: mission.MissionCustomValue | None = None

    target_submission_id: int
    target_mission_custom_value: mission.MissionCustomValue
    value_a: Value
    value_b: Value


class CaptureLocalPlayer(Model):
    character_unique_name: str


class CaptureNPCToCharacter(Model):
    group_id: FixedValue[int] | Dynamic | None = None
    group_npc_id: FixedValue[int] | Dynamic | None = None
    character_unique_name: Value[str] | None = None
    release_if_performance_end: bool = True
    target_type: target.Target | None = None
    task_enabled: bool = True


class ChangeDynamicOptionalBlock(Model):
    block_key: str


class ChangeHeartDialModelByScript(Model):
    script_id: FixedValue[int]


class ChangeHeroType(Model):
    pass


class ChangePropState(Model):
    pass


class ChangeTeamLeader(Model):
    pass


class ChangeTrackingMission(Model):
    tracking_main_mission_id: int


class ChangeTrackVirtualCameraFollowAndAim(Model):
    area_name: str
    track_name: str
    camera_name: str
    target_area_name: str
    follow_target_anchor_name: str
    look_at_target_anchor_name: str


class CharacterDisableLookAt(Model):
    character_unique_name: str
    disable: bool = True


class CharacterHeadLookAt(Model):
    character_unique_name: str
    target_area_name: str | None = None
    target_character_unique_name: str | None = None
    target_anchor_name: str | None = None
    target_character_attach_point: camera.AttachPoint | None = None
    duration: int | None = None
    keep_tracking: bool = True
    constraint: dict[None, None]


class CharacterHeadStopLookAt(Model):
    character_unique_name: str
    wait_until_finish: bool = False
    task_enabled: bool = True


class CharacterNavigateTo(Model):
    character_unique_name: str
    area_name: str
    anchor_name: str
    motion_flag: typing.Literal["Run", "Walk"] | None = None
    wait_until_finish: bool = True
    avoid_others: bool = True
    turn_in_place: bool = False
    dont_turn_in_place_in_end: bool = False
    duration: int | None = None


class CharacterSteerTo(Model):
    character_unique_name: str
    target_character_unique_name: str


class CharacterStopFreeStyle(Model):
    character_unique_name: str | None = None
    target_type: target.Target | None = None
    normalized_transition_duration: float | None = None
    task_enabled: bool = True


class CharacterTriggerAnimState(Model):
    character_unique_name: Value[str] | Custom
    target_alias: target.Target | None = None
    force_start: bool = False
    anim_state_name: str
    normalized_time_start: float | None = None
    normalized_transition_duration: float | None = None
    normalized_time_wait: float | None = None
    task_enabled: bool = True


class CharacterTriggerFreeStyle(Model):
    character_unique_name: str | None = None
    target_alias: target.Target | None = None
    disable_anim_event: bool = False
    force_start: bool = True
    story_avatar_id: str
    normalized_time_start: float | None = None
    normalized_transition_duration: float | None = None
    normalized_time_wait: float | None = None
    story_motion_id: int | None = None
    task_enabled: bool = True


class CharacterTriggerFreeStyleGraph(Model):
    target_alias: target.Target
    graph_name: Value[str]


class CheckMainMissionFinishedInCurrentVersion(Model):
    main_mission_id: int
    on_current_version_finished_task: list["Task"]
    on_not_current_version_finished_task: list["Task"]


class ClearDialogCamera(Model):
    pass


class ClearNpcDistanceTrigger(Model):
    group_id: int
    group_npc_id: int


class ClearTalkUI(Model):
    hide_control_btns: bool = False
    success_without_talk: bool = False


class ClientFinishMission(Model):
    submission_id: int | None = None


class ClosePage(Model):
    page_names: list[str]
    page_root_names: list[None]
    is_silent_exit: bool = True


class CollectDataConditions(Model):
    task_id_list: list[int] | None = None
    main_mission_id_list: list[int] | None = None
    performance_id_list: list[int]
    performance_idds_list: typing.Annotated[
        list[Value[typing.Literal["E"]]] | None, pydantic.Field(alias="PerformanceIDDsList")
    ] = None
    custom_value_main_mission_id_list: list[int] | None = None
    task_enabled: bool = True


class ConsumeMissionItem(Model):
    sub_mission_id: int
    is_auto_consume: bool = False
    is_show_consume_finish_tips: bool = False
    desc: Text | None = None
    simple_talk: Empty | None = None


class ConsumeMissionItemPerformance(Model):
    sub_mission_id: int
    desc: Text | None = None
    on_submit_confirm: list["Task"]
    on_submit_cancel: list["Task"] | None = None
    simple_talk: dict[None, None] | None = None


class ConsumeOrigamiItem(Model):
    colony_id: FixedValue[int]
    desc: Text
    on_submit_confirm: list["Task"]
    on_submit_cancel: list["Task"]
    simple_talk: dict[None, None]


class ConvinceInitialize(Model):
    base_anchor: typing.Literal["ConvinceBase"]
    left_actor_unique_name: str
    right_actor_unique_name: typing.Literal["PlayerBoy_00_C00"]
    left_anchor_data_key: typing.Literal["Male"]
    right_anchor_data_key: typing.Literal["Player"]
    left_bg_texture: str
    right_bg_texture: str
    left_text_name_list: list[Text]
    turn_num: int
    init_h_p: typing.Literal[2] | None = None
    skill_types: list[str]
    skill_use_num: typing.Literal[2] | None = None
    convince_gameplay_n_p_c_id: int | None = None


class ConvinceMoveCurrTurnOption(Model):
    pass


class ConvinceMoveNextTurn(Model):
    pass


class ConvinceMovePrevTurn(Model):
    pass


class ConvinceMoveTurn(Model):
    turn_index: int | None = None


class ConvincePlayOptionTalk(Model):
    option_list: list[talk.OptionTalkInfo]


class ConvinceShowToast(Model):
    show_hint: bool = False
    toast_type: typing.Literal["Failure", "SkillCast", "Success"] | None = None
    hint_text: Text | None = None
    title_text: Text | None = None


class ConvinceWaitAllTurnFinish(Model):
    turn_index: int | None = None


class ConvinceWaitTrickSkill(Model):
    trick_skill_type: typing.Literal["DoubleEffect", "Rollback", "SkipCurrent"]


class ConvinceWaitTurnBegin(Model):
    turn_index: int | None = None


class CreateAirline(Model):
    group_id: int | None = None
    prefab_path: str


class CreateLevelAreas(Model):
    asset_path: Value[pathlib.Path]
    task_enabled: bool = True


class CreateNPC(Model):
    group_id: FixedValue[int] | Dynamic | None = None
    group_npc_id: FixedValue[int] | Dynamic | None = None
    npc_unique_name: typing.Annotated[Value[str] | None, pydantic.Field(alias="NPCUniqueName")] = None
    create_list: list[performance.Create] | None = None
    task_enabled: bool = True


class CreatePhoneOnCharacter(Model):
    is_destroy: bool = False
    group_id: int | None = None
    group_npc_id: int | None = None
    target_type: target.Target | None = None


class CreateProp(Model):
    group_id: FixedValue[int]
    group_prop_id: FixedValue[int]
    create_list: list[performance.GroupEntityInfo] | None = None


class CreateTrialPlayer(Model):
    pass


class DebateInitialize(Model):
    class SpecialItem(BaseModel):
        item_id: int | None = None
        trigger_custom_string: str | None = None

    class TestimonySetting(BaseModel):
        index: int | None = None
        testimony_type: typing.Literal["LastStatement"] | None = None
        timeline_clip_name: typing.Literal["0", "1", "2", "3", "4", "5"]
        can_ask: bool = False
        last_to_begin_talk_sentence_id: typing.Literal[800325736] | None = None
        ask_custom_string: str | None = None
        can_submit_item: bool = False
        item_id_list: list[int] | None = None
        special_item_list: list["DebateInitialize.SpecialItem"] | None = None
        item_default_custom_string: str | None = None

    testimony_timeline_path: str
    show_start_toast: bool = True
    testimony_setting_list: list[TestimonySetting]
    ui_type: typing.Literal["Explain", "Question"] | None = None


class DebateReturnTestimony(Model):
    pass


class DebateShowToast(Model):
    toast_type: typing.Literal["Failure", "Success"]


class DestroyCurvePropGroupPuzzle(Model):
    unique_name: Value[str]


class DestroyNPC(Model):
    group_id: int | None = None
    group_npc_id: int | None = None
    hide: bool = False
    target_type: target.Target | None = None
    destroy_list: list[performance.GroupEntityInfo] | None = None


class DestroyProp(Model):
    target_type: target.Target
    id: FixedValue[int] | None = None
    group_id: FixedValue[int] | None = None
    destroy_list: list[performance.GroupEntityInfo] | None = None
    task_enabled: bool = True


class DestroyTrialPlayer(Model):
    pass


class EnableBillboard(Model):
    target_type: target.Target
    enable: bool = False


class EnableNPCMonsterAI(Model):
    enable: bool = False
    group_id: int | None = None
    group_monster_ids: typing.Annotated[list[int], pydantic.Field(alias="GroupMonsterIDs")]
    target_type: target.Target | None = None
    unique_names: list[None]
    reset_state_on_disable: bool = True
    task_enabled: bool = True


class EnablePerformanceMode(Model):
    enable: bool = False


class EndDialogueEntityInteract(Model):
    override_tasks: camera.OverrideTasks | None = None


class EndPerformance(Model):
    pass


class EndPropInteract(Model):
    task_enabled: bool = True


class EnterFlipperLightDeviceControl(Model):
    target_device: target.Target


class EnterMap(Model):
    entrance_id: int | None = None
    group_id: int | None = None
    anchor_id: int | None = None


class EnterMapByCondition(Model):
    entrance_id: FixedValue[int]


class ExitTransitionLoadingUI(Model):
    pass


class FinishLevelGraph(Model):
    make_owner_entity_die: bool = False


class FinishPerformanceMission(Model):
    key: str
    main_mission_id: int | None = None
    keep_screen_transfer_until_group_refresh: bool = False
    use_specified_loading: bool = False
    stratage_type: typing.Literal["Plain", "StoryLine"] | None = None


class FinishRogueAeonTalk(Model):
    pass


class ForceSetDialogCamera(Model):
    target_type: target.Target


class GuessTheSilhouetteResult(Model):
    silhouette_id: int
    is_executing: typing.Literal[True]


class HeliobusSNSQuickPost(Model):
    post_id: int | None = None
    on_post_: list["Task"]
    post_id_ds: typing.Annotated[Custom | None, pydantic.Field(alias="PostID_DS")] = None
    on_cancel: list["Task"] | None = None


class HideAllEntity(Model):
    class Group(BaseModel):
        GroupID: int
        GroupNpcID: int

    is_hide: bool = False
    hide_npc: typing.Annotated[typing.Literal[True], pydantic.Field(alias="HideNPC")]
    hide_prop: typing.Literal[True]
    not_hide_entity: list[Group]


class HideEntity(Model):
    target: target.Target
    is_hide: bool = False
    task_enabled: bool = True


class HideEntityV2(Model):
    target: target.Target
    is_hide: bool = False


class HideSummonUnit(Model):
    summon_unit: target.Target
    hide: bool = True


class HideTopPage(Model):
    hide: bool = False


class HideWaypointByProp(Model):
    target_type: target.Target | None = None
    use_owner_entity: bool = False
    group_id: FixedValue[int] | None = None
    instance_id: FixedValue[int] | None = None
    prop_key: Custom | None = None
    on_name_board: bool = False


class LensDistortionCurveEffect(Model):
    x_multiplier: int | None = None
    y_multiplier: int | None = None
    intensity: int
    scale: float | None = None
    x_curve_path: str
    y_curve_path: str
    intensity_curve_path: str
    scale_curve_path: str | None = None
    duration: float


class LevelAudioState(Model):
    group_name: str
    state_name: Value[str]


class LevelPerformanceInitialize(Model):
    performance_type: performance.Type
    area_prefab_path: str | None = None
    mute_sfx: typing.Annotated[bool, pydantic.Field(alias="MuteSFX")] = False
    create_character_list: list[performance.CreateCharacter] | None = None
    capture_npc_list: typing.Annotated[list[performance.CaptureNPC] | None, pydantic.Field(alias="CaptureNPCList")] = (
        None
    )
    hide_npc: typing.Annotated[bool, pydantic.Field(alias="HideNPC")] = False
    entity_visiable_list: list[performance.EntityVisiable | Empty] | None = None
    hide_municipal_crowd: bool = True
    hide_municipal_pedestrian: bool = True
    hide_municipal_other: bool = True
    hide_monster: bool = True
    hide_prop: bool = False
    prop_visiable_list: list[performance.PropVisiable | Empty] | None = None
    hide_local_player: bool = False
    first_camera_anchor: str | None = None
    use_new_streaming_source_type: bool = False
    streaming_sources_in_black_mask: list[str] | None = None
    streaming_sources_after_black_mask: list[str] | None = None
    mark_streaming_items: list[None] | None = None
    reset_environment: bool = True
    reset_monster: bool = True
    audio_state_list: list[None] | None = None


class LockCurrentTeleportAction(Model):
    pass


class LockPhotoIdentifyHint(Model):
    pass


class LockPlayerControl(Model):
    lock_camera_control: bool = True


class LockTeamLeader(Model):
    pass


class NpcPossession(Model):
    class PossessionInfo(BaseModel):
        name: str
        is_override: bool = False
        local_position: Axis | None = None
        attach_point: str | None = None

    group_id: FixedValue[int] | None = None
    group_npc_id: FixedValue[int] | None = None
    npc_unique_name: str | None = None
    possession_info: PossessionInfo
    target_type: target.Target | None = None
    is_delete: bool = False


class NpcSetupTrigger(Model):
    target_type: target.Target
    trigger_id: int
    disable_after_triggered: bool = False
    range: float | None = None
    on_trigger_enter: list["Task"] | None = None
    on_trigger_exit: list["Task"] | None = None
    target_types: list[str] | None = None


class NpcToPlayerDistanceTrigger(Model):
    group_id: int
    group_npc_id: int
    near_distance: int | None = None
    near_task: list["Task"] | None = None
    far_distance: int | None = None
    far_task: list["Task"] | None = None


class MonsterResearchSubmit(Model):
    activity_monster_research_id: int
    on_question1: list["Task"]
    on_question2: list["Task"] | None = None
    on_question3: list["Task"] | None = None
    on_cancel: list["Task"]


class MoveVirtualCameraOnDollyPath(Model):
    area_name: str
    anchor_name: str
    start_point: float
    end_point: float | None = None
    curve_name: str
    duration: int


class OnMuseumPerformanceBegin(Model):
    on_performance_begin: list["Task"]
    area_id: int


class OnMuseumPerformanceEnd(Model):
    pass


class OpenRaid(Model):
    raid_id: int
    on_cancel: list["Task"] | None = None
    is_skip_ui: bool = False


class OpenTreasureChallenge(Model):
    raid_id: int | None = None
    dynamic_raid_id: int | None = None
    on_enter: list["Task"] | None = None
    on_cancel: list["Task"] | None = None


class OverrideEndTransferColor(Model):
    color: typing.Literal["White"]


class OverrideEndTransferType(Model):
    black_type: excel.performance.BlackType | None = None


class OverrideFinishActionAutoTransfer(Model):
    submission_id: int
    transfer_type: typing.Literal["Black"] | None = None


class OverridePerformanceEndCrack(Model):
    end_with_crack: bool = False


class PerformanceEndBlackText(Model):
    talk_sentence_id: int


class PerformanceEndSeq(Model):
    class Case(BaseModel):
        Case: int | None = None
        force_close_black: bool = False
        on_success: list["Task"]

    cases: list[Case | Empty] | None = None
    before_cases: list["Task"] | None = None


class PerformanceExtendEndBlack(Model):
    extend_time: float | None = None


class PerformanceTransition(Model):
    switch_in_time: float | None = None
    switch_keep_time: float | None = None
    switch_out_time: float | None = None
    text_enabled: bool = False
    talk_sentence_id: int | None = None
    not_auto: bool = False
    create_npc_list: list[performance.CreateNpc] | None = None
    capture_npc_list: list[performance.CaptureNpc] | None = None
    destroy_npc_list: list[performance.DestroyNpc] | None = None
    create_prop: performance.CreateProp | None = None
    destroy_prop: performance.DestroyProp | None = None
    adv_create_group_entity: performance.AdvGroupEntity | None = None
    adv_destroy_group_entity: performance.AdvGroupEntity | None = None
    disactive_v_cam_on_graph_end: bool = True
    active_virtual_camera: camera.ActiveVirtualCamera
    active_template_virtual_camera: camera.ActiveVirtualCamera | None = None
    switch_character_anchor: performance.SwitchCharacterAnchor
    adv_npc_face_to_player: performance.AdvNpcFaceToPlayer | None = None
    wait_streaming_finish: bool = False
    task_enabled: bool = True


class PhotoGraphAimTarget(Model):
    aim_target_type: target.Target
    is_aim: bool = False
    aim_identify_type: typing.Literal["Manual"] | None = None
    aim_tag_extra_offset: float | None = None


class PhotoGraphShowIdentifyResult(Model):
    is_identify_success: bool = False
    is_show_toast: typing.Literal[True]
    toast_text: Text
    is_show_aim: bool = False
    photo_graph_mode: typing.Literal["IdentifyUAV"] | None = None


class PhotoGraphWaitIdentifyFinish(Model):
    wait_target_type: target.Target
    wait_all: bool = False
    on_identify_finish: list["Task"] | None = None
    on_identify_failed: list["Task"] | None = None
    on_preview_finish: list["Task"] | None = None


class PlayAeonTalk(Model):
    aeon_talk_id: typing.Annotated[int, pydantic.Field(validation_alias="AeonTalkId")]
    aeon_talk_count: int
    simple_talk_list: list[talk.RogueSimpleTalk]


class PlayAndWaitRogueSimpleTalk(Model):
    simple_talk_list: list[talk.RogueSimpleTalk]


class PlayAndWaitSimpleTalk(Model):
    black_mask: bool = False
    keep_display: bool = True
    need_fade_black_mask: bool = False
    use_background: bool = False
    skip_first_talk_bg_fade_in: bool = False
    backgrounds: list[talk.Background] | None = None
    use_target_behavior: bool = False
    target_behaviors: list[talk.TargetBehavior] | None = None
    simple_talk_list: list[talk.SimpleTalk]


class PlayerForceWalk(Model):
    force_walk: bool = False


class PlayerRemoteControlOtherEntity(Model):
    target_entity: target.Target | None = None
    special_n_p_c_id: int | None = None
    is_cancel: bool = False
    use_local_player_position: bool = False
    recover_control_entity_position: bool = False
    support_rush: bool = True
    sync_position_to_server: bool = False
    leave_player_stub_inplace: bool = False
    player_stub_animation: Value[typing.Literal["LookatPhoneBS"]] | None = None
    force_position_and_rotation: bool = False
    level_area_key: Custom | None = None
    show_release_button: bool = False


class PlayerSelectMotionMode(Model):
    class MotionMode(enum.Enum):
        ForbidFastRun = "ForbidFastRun"
        ForceWalk = "ForceWalk"

    motion_mode: MotionMode | None = None


class PlayFullScreenTransfer(Model):
    class TextInfo(BaseModel):
        not_auto: bool = False
        play_voice: bool = False
        text_list: list[talk.SimpleTalk]

    class ScrTrfActPerformance(Model):
        create_npc: performance.CreateNpc
        destroy_npc: performance.DestroyNpc
        create_prop: performance.CreateProp
        destroy_prop: performance.DestroyProp
        capture_npc: list[performance.CaptureNpc]
        switch_character_anchor: performance.SwitchCharacterAnchor
        active_virtual_camera: camera.ActiveVirtualCamera
        active_template_virtual_camera: camera.ActiveVirtualCamera
        adv_npc_face_to_player: performance.AdvNpcFaceToPlayer
        wait_streaming_finish: bool = False

    class ScrTrfActPerformanceGroup(Model):
        adv_create_group_entity: performance.AdvGroupEntity
        adv_destroy_group_entity: performance.AdvGroupEntity
        capture_npc: list[performance.CaptureNpc]
        switch_character_anchor: performance.SwitchCharacterAnchor
        active_virtual_camera: camera.ActiveVirtualCamera
        active_template_virtual_camera: camera.ActiveVirtualCamera
        adv_npc_face_to_player: performance.AdvNpcFaceToPlayer
        wait_streaming_finish: bool = False

    class ScrTrfActTaskList(Model):
        task_list: list["Task"]

    __Action = typing.Annotated[
        typing.Annotated[ScrTrfActPerformance, pydantic.Tag("ScrTrfActPerformance")]
        | typing.Annotated[ScrTrfActPerformanceGroup, pydantic.Tag("ScrTrfActPerformanceGroup")]
        | typing.Annotated[ScrTrfActTaskList, pydantic.Tag("ScrTrfActTaskList")],
        pydantic.Discriminator(get_discriminator),
    ]

    type: typing.Literal["None", "White"] | None = None
    prev_duration: float | None = None
    keep_duration: float | None = None
    post_duration: float | None = None
    keep_display: bool = False
    text_info: TextInfo | None = None
    end_task_after_ui_close: bool = False
    action: list[__Action] | None = None


class PlayNPCBubbleTalk(Model):
    bubble_talk_info_list: list[talk.NPCBubbleTalk]
    instant_finish: bool = True
    is_loop: bool = False
    loop_interval: int | None = None
    unique_id: int | None = None
    id: int | None = None


class PlayNPCSingleBubbleTalk(Model):
    target_type: target.Target
    auto_skip_time: int | None = None
    talk_sentence_id: FixedValue[int] | Dynamic
    unique_id: int | None = None


class PlayMazeButtonEffect(Model):
    enable: bool = False
    btn_type: typing.Literal["MazeSkill"] | None = None


class PlayMessage(Model):
    message_section_id: int
    show_notice: bool = True


class PlayMissionTalk(Model):
    is_voice_3d: bool = False
    resume_after_interrupt: bool = False
    start_sentence_id: FixedValue[int] | None = None
    sub_mission_id_for_resume: int | None = None
    voice_3d_target_type: target.Target | None = None
    end_sentence_id: FixedValue[int] | None = None
    simple_talk_list: list[talk.SimpleTalk]
    task_enabled: bool = True


class PlayMultiVoiceTalk(Model):
    talk_sentence_id: int


class PlayMunicipalChat(Model):
    class MunicipalChatEntityInfo(BaseModel):
        typ: typing.Annotated[typing.Literal["RPG.GameCore.MunicipalChatEntityInfo"], pydantic.Field(alias="$type")]
        unique_name: str
        group_instance_id: int

    new_municipal_chat_config_path: str
    new_municipal_chat_entity_infos: Value[list[MunicipalChatEntityInfo]]
    municipal_chat_name: str


class PlayOptionTalk(Model):
    option_list: list[talk.OptionTalkInfo]
    hide_button_auto: bool = False
    hide_selected: bool = False
    trigger_string: str | None = None
    trigger_string_when_all_selected: bool = False


class PlayOrigamiTraceTalk(Model):
    class TalkInfo(BaseModel):
        simple_talk_list: list[talk.SimpleTalk]
        target_behaviors: list[None] | None = None

    class Talk(BaseModel):
        group_id: FixedValue[int]
        talk_info: "PlayOrigamiTraceTalk.TalkInfo"

    colony_id: FixedValue[int]
    talk_list: list[Talk]


class PlayRogueOptionTalk(Model):
    option_list: list[talk.RogueOptionTalk]


class PlayRogueSimpleTalk(Model):
    simple_talk_list: list[talk.RogueSimpleTalk]


class PlayScreenCrack(Model):
    effect_path: str | None = None
    screen_crack_ui: bool = False
    unique_effect_name: typing.Literal["ScreenCrack"]
    execute_on_skip: bool = False


class PlayScreenTransfer(Model):
    class TransferFullDuration(BaseModel):
        prev_duration: float | None = None
        keep_duration: float | None = None
        post_duration: float | None = None

    type: typing.Literal["None"] | None = None
    mode: typing.Literal["DirectlySet", "FullTransfer", "SwitchOut"] | None = None
    custom_time: float | None = None
    transfer_full_duration: TransferFullDuration | None = None
    keep_display: bool = False
    mask_alpha: int | None = None
    text_enabled: bool = False
    talk_sentence_id: int | None = None
    not_auto: bool = False
    task_enabled: bool = False


class PlaySimpleTalk(Model):
    use_background: bool = False
    backgrounds: list[talk.Background] | None = None
    black_mask: bool = False
    keep_display: bool = True
    simple_talk_list: list[talk.SimpleTalk]


class PlaySequenceDialogue(Model):
    dialogues: list["Task"]


class PlayTimeline(Model):
    class Type(enum.Enum):
        Cutscene = "Cutscene"
        Discussion = "Discussion"
        Story = "Story"

    timeline_name: str
    type: Type | None = None
    parameters: list[None] | None = None
    release_volume: bool = False
    task_enabled: bool = True


class PlayTimelinePrefab(Model):
    prefab_path: str
    area_name: Custom
    anchor_name: Custom


class PlayVideo(Model):
    video_id: int
    is_mute_bgm: bool = True
    without_change_audio: bool = False


class PlayVoice(Model):
    voice_ids: typing.Annotated[list[int], pydantic.Field(alias="VoiceIDs")]
    target_type: target.Target | None = None
    interval_time: int | None = None


class PlayVoice_Sequence(Model):
    voice_ids: typing.Annotated[list[int], pydantic.Field(alias="VoiceIDs")]


class PPFilterStackEffect(Model):
    active: bool = True
    priority_group: typing.Literal["MazeGroupHigh", "PerformanceGroup"] | None = None
    priority: typing.Literal["High", "Middle"] | None = None
    start_rate: float | None = None
    rate: float | None = None
    duration: float | None = None
    recover_duration: float | None = None
    asset_path: str | None = None
    mute_audio_event: bool = False
    is_distance_attenuation_on: bool = False
    target_type: target.Target | None = None
    max_attenuation_distance: int | None = None
    task_enabled: bool = True


class PredicateTaskList(Model):
    predicate: predicate.Predicate
    success_task_list: list["Task"] | None = None
    failed_task_list: list["Task"] | None = None


class PredicateTaskListWithFail(Model):
    predicate_: predicate.Predicate | None = None
    success_task_list: list["Task"] | None = None


class PropDestruct(Model):
    target_type: target.Target


class PropEnableCollider(Model):
    class OpType(enum.Enum):
        ColliderOnly = "ColliderOnly"
        TriggerOnly = "TriggerOnly"

    class TriggerSelect(enum.Enum):
        CustomTrigger = "CustomTrigger"
        HintTrigger = "HintTrigger"
        PropInteractionTrigger = "PropInteractionTrigger"
        PropOptionTrigger = "PropOptionTrigger"

    op_type: typing.Annotated[OpType | None, pydantic.Field(alias="OPType")] = None
    enabled: bool = False
    specified_relative_paths: list[str] | None = None
    trigger_select: TriggerSelect | None = None
    custom_trigger_name: str | None = None
    target_type: target.Target
    task_enabled: bool = False


class PropMoveTo(Model):
    duration: FixedValue[float] | None = None
    speed: FixedValue[int] | None = None
    area_name: str | None = None
    level_area_key: Custom | None = None
    anchor_name: str | None = None
    wait_finish: bool = False
    use_curve_data: bool = False
    target_type: target.Target


class PropReqInteract(Model):
    target_type: target.Target
    interact_id: FixedValue[int]


class PropSetupHitBox(Model):
    collider_relative_path: typing.Literal["Hitbox"] | None = None
    on_be_hit: list["Task"]
    target_type: target.Target


class PropSetupTrigger(Model):
    target_type: target.Target
    is_single: bool = False
    target_entity_type: target.EntityType | None = None
    target_group_id: FixedValue[int] | Dynamic | None = None
    target_id: FixedValue[int] | Dynamic | None = None
    target_types: list[str] | None = None
    collider_relative_path: str | None = None
    destroy_after_triggered: bool = False
    disable_after_triggered: bool = False
    on_trigger_enter: list["Task"] | None = None
    on_trigger_exit: list["Task"] | None = None
    task_enabled: bool = True
    block_dialogue_in_range: bool = False
    destroy_after_graph_end: bool = False
    on_exit_filter: predicate.Predicate | None = None
    trigger_by_fake_avatar: bool = False
    skip_fake_avatar: bool = True
    block_change_fake_avatar_callback: bool = False


class PropSetupUITrigger(Model):
    class ColliderRelativePath(enum.Enum):
        BackwardCollider = "BackwardCollider"
        ForwardCollider = "ForwardCollider"
        LeftCollider = "LeftCollider"
        RightCollider = "RightCollider"
        Trigger = "Trigger"
        TriggerUIBtn = "TriggerUIBtn"

    collider_relative_path: ColliderRelativePath | None = None
    destroy_after_triggered: bool = False
    disable_after_triggered: bool = False
    disable_when_triggered: bool = False
    button_icon: str | None = None
    icon_type: talk.OptionIconType | None = None
    button_text: Text | None = None
    button_text_custom: Value[str] | Custom | None = None
    button_callback: list["Task"]
    consider_angle_limit: bool = False
    force_interact_in_danger: bool = False
    interact_angle_range: int | None = None
    override_target_types: list[typing.Literal["LocalPlayer"]] | None = None
    trigger_by_fake_avatar: bool = False
    skip_fake_avatar: bool = True
    on_enter_filter: predicate.Predicate | None = None
    target_type: target.Target


class PropSetVisibility(Model):
    specified_relative_paths: list[str] | None = None
    target_type: target.Target
    visible: bool = False


class PropStateChangeListenerConfig(Model):
    from_state: predicate.PropState | None = None
    to_state: predicate.PropState | None = None
    from_any_state: bool = False
    on_change: list["Task"]
    target_type: target.Target


class PropStateExecute(Model):
    target_type: target.Target
    execute: list["Task"] | None = None
    state: str | None = None


class PropTriggerAnimState(Model):
    anim_state_name: str
    fixed_transition_duration: bool = True
    transition_duration: int | None = None
    wati_anim_finish: bool = False
    target_type: target.Target


class PuzzleSetAnimatorParams(Model):
    class Param(BaseModel):
        animator_path: typing.Literal["MirrorBack", "MirrorFront", "Reflection"]
        param_name: typing.Literal["Chaos"]
        param_type: typing.Literal["Int"]

    target_type: target.Target
    params: list[Param]


class QuestGetReward(Model):
    quest_id_list: list[FixedValue[int]]


class RadialBlurEffect(Model):
    active: bool = True
    target_type: target.Target | None = None
    duration: float | None = None
    blur_radius: typing.Literal[1] | None = None
    iteration: int | None = None
    blur_start: float | None = None
    blur_feather: float | None = None


class RaidSceneTransfer(Model):
    pass


class RandomConfig(Model):
    odds_list: list[FixedValue[float]]
    task_list: list["Task"]
    continuous_not_repeat: bool = False
    random_mask_target: target.Target | None = None


class ReleaseCacheUI(Model):
    prefab_path: str


class ReleaseCharacter(Model):
    character_unique_name: str


class ReleaseEnvProfileForStory(Model):
    pass


class RemoveAirline(Model):
    group_id: int | None = None
    prefab_path: str


class RemoveBattleEventData(Model):
    pass


class RemoveEffect(Model):
    target_type: target.Target | None = None
    effect_path: str | None = None
    unique_effect_name: str | None = None
    attach_point_name: str | None = None
    flags: list[str] | None = None
    unbind: bool = False
    is_need_fade_out: bool = True


class RemoveLevelAreas(Model):
    area_name: Value[str] | Custom
    task_enabled: bool = True


class RemoveMazeBuff(Model):
    target_type: target.Target
    id: int


class RemoveStreamingSource(Model):
    streaming_source: str


class RemoveVirtualLineupBindPlane(Model):
    pass


class ReplaceTrialPlayer(Model):
    pass


class ReplaceVirtualTeam(Model):
    pass


class ResetBillboardInfo(Model):
    target_entity_type: target.EntityType
    id: int
    group_id: int


class ResetMissionAudioState(Model):
    reset_bgm_emotion_state: bool = False
    reset_sound_effect_state: bool = False


class ResetMissionWayPoint(Model):
    sub_mission_id: int


class ResetPhotoGraphTargets(Model):
    bind_name: Value[str]


class RestoreTrackingMission(Model):
    pass


class RetrySwordTrainingFinalBattle(Model):
    is_retry: bool = False


class ReturnToLoginPage(Model):
    wait_talk_mission_key: str


class RogueFinish(Model):
    pass


class RogueShowSelectMainPage(Model):
    pass


class SaveMessage(Model):
    message_section_id: int


class SceneGachaListener(Model):
    grand_reward_callback: list["Task"] | None = None
    small_reward_callback: list["Task"]


class SelectMissionItem(Model):
    sub_mission_id: int | None = None
    only_performance: bool = True
    item_id_list: list[int]
    item_hidden_id_list: list[int] | None = None
    item_invisible_id_list: list[int] | None = None
    item_select: list[select_mission_item.ItemSelect] | None = None
    slot_num: int | None = None
    info_text: Text | None = None
    simple_talk: select_mission_item.SimpleTalk | None = None
    mask_error_item: bool = False
    on_submit_succeed: list["Task"] | None = None
    on_submit_fail: list["Task"] | None = None
    on_submit_cancel: list["Task"] | None = None


class SelectorConfig(Model):
    task_list: list["Task"]


class SequenceConfig(Model):
    task_list: list["Task"]


class SetAdvAchievement(Model):
    achievement_id: int | None = None
    quest_id: int | None = None
    group_id: int | None = None
    instance_id: int | None = None


class SetAllMissionWaypointsVisiable(Model):
    is_visiable: bool = False


class SetAllRogueDoorState(Model):
    pass


class SetAsRogueDialogue(Model):
    pass


class SetAudioEmotionState(Model):
    state_name: str | None = None
    reset_to_floor_default: bool = False
    sub_mission_id: int | None = None


class SetBattleBGMState(Model):
    state_name: Value[str]


class SetBillboardInfo(Model):
    target_entity_type: target.EntityType | None = None
    id: int | None = None
    group_id: int | None = None
    name: Text | None = None
    title: Text | None = None
    map_icon_type: int | None = None
    edit_height: bool = False
    min_height: float | None = None
    max_height: float | None = None
    board_show_list: list[int] | None = None
    show_distance: list[int] | None = None


class SetCharacterAtlasFaceEmotion(Model):
    character_unique_name: str | None = None
    mesh_name: typing.Literal["Body"] | None = None
    emotion_index: int | None = None


class SetCharacterShadowFactor(Model):
    enable_factor: bool = False
    only_enable_when_use_shadow_probe: bool = False


class SetCharacterVisible(Model):
    character_unique_name: str | None = None
    target_type: target.Target | None = None
    visible: bool = False


class SetClockBoyEmotion(Model):
    class AtlasEmotion(BaseModel):
        mesh_name: typing.Literal["Eye"] | None = None
        emotion_index: int | None = None

    class Clock(BaseModel):
        hour: int
        minute: int

    target_type: target.Target
    atlas_emotions: list[AtlasEmotion]
    clock: Clock


class SetEffectAnimatorTrigger(Model):
    unique_effect_name: str
    trigger_name: typing.Literal["TriggerVisionClose"]


class SetEntityTalkEnable(Model):
    target: target.Target
    enable_talk: bool = False


class SetEntityVisible(Model):
    target_type: target.Target
    visible: bool = False
    mute_collider_when_invisible: bool = True
    mute_trigger_when_visible: bool = False


class SetFloorCustomBool(Model):
    class BoolValue(BaseModel):
        value: bool = False

    name: Value[str]
    value: BoolValue


class SetFloorCustomFloat(Model):
    class ExtraInfo(BaseModel):
        lock: bool = False

    name: Value[str]
    value: FixedValue[float]
    extra_info: ExtraInfo | None = None


class SetFloorCustomFloatV2(Model):
    name: Value[str]
    value: FixedValue[int]


class SetFloorCustomString(Model):
    name: Value[str]
    value: Value[str]


class SetFloorSavedValue(Model):
    pass


class SetForceStreamingThisFrame(Model):
    start_loading_tick: typing.Literal[True]


class SetFuncBtn(Model):
    custom_string: Value[str] | None = None
    show_btn_effect: bool = False


class SetHLODSwitchDelay(Model):
    default_delay: bool = False
    no_delay: bool = False


class SetHudTemplate(Model):
    template_id: int
    enable_template: bool = False


class SetLoadingStratageType(Model):
    stratage_type: typing.Literal["Legacy", "Plain", "StoryLine"]
    loading_type: typing.Literal["RefreshLoading"] | None = None
    roll_back_when_mission_fail: bool = False
    submission_id: int | None = None


class SetLocalPlayerDitherAlpha(Model):
    dither_alpha: typing.Literal[1] | None = None
    duration: float | None = None
    task_enabled: bool = True


class SetMissionAudioState(Model):
    set_bgm_emotion_state: bool = False
    bgm_emotion_state_name: excel.mission.EmotionState | None = None
    set_default_bgm_emotion_state: bool = False
    set_sound_effect_state: bool = False
    sound_effect_state_name: str | None = None
    set_default_sound_effect_state: bool = False


class SetMissionCustomValue(Model):
    submission_id: int
    mission_custom_value: mission.MissionCustomValue | None = None
    custom_value: int | None = None


class SetMissionWayPoint(Model):
    sub_mission_id: int
    overide_mission_way_point_type: bool = False
    mission_way_point_type: target.EntityType | None = None
    overide_way_point_floor_id: bool = False
    way_point_floor_id: int | None = None
    overide_way_point_group_id: bool = False
    way_point_group_id: int | None = None
    overide_way_point_entity_id: bool = False
    way_point_entity_id: int | None = None
    overide_way_point_show_range_min: bool = False
    way_point_show_range_min: int | None = None
    overide_map_waypoint_range: bool = False
    map_waypoint_range: int | None = None


class SetMunicipalEnable(Model):
    visible: bool = False


class SetNPCMonstersVisible(Model):
    pass


class SetNpcStatus(Model):
    class Status(enum.Enum):
        FollowByPlayer = "FollowByPlayer"
        FollowPlayer = "FollowPlayer"
        Patrol = "Patrol"
        PetSearch = "PetSearch"

    target_type: target.Target
    status: Status | None = None
    task_enabled: bool = True


class SetNpcWaypath(Model):
    target_type: target.Target
    UsageType: typing.Literal["TaskFollow"] | None = None


class SetPerformanceResult(Model):
    value: int | None = None


class SetRogueRoomFinish(Model):
    pass


class SetSpecialVisionOn(Model):
    is_on: bool = False
    vision_type: typing.Literal["MemoryVision", "PlayerSearchSneakMonster"] | None = None
    vision_effect_type: typing.Literal["Empty", "NishastagaVision", "SearchMonster"] | None = None
    camera_effect_type: typing.Literal["MemoryVision"] | None = None
    is_infinite_time: bool = False
    smell_prop: dict[None, None] | None = None


class SetStageItemState(Model):
    class Item(BaseModel):
        block_alias: str
        prefab_alias: str

    item_list: list[Item]
    enable_state: bool = False
    task_enabled: bool = True


class SetTargetEntityFadeWithAnim(Model):
    target_type: target.Target
    target_value: typing.Literal[1] | None = None
    duration: float | None = None


class SetTargetUniqueName(Model):
    target_type: target.Target
    unique_name: str


class SetTextJoinValue(Model):
    text_join_id: int
    value: int | None = None
    show_input_dialog: bool = False
    on_cancel: list["Task"] | None = None


class SetTraceOrigamiFlag(Model):
    pass


class SetTrackingMission(Model):
    main_mission_id: int | None = None


class SetVirtualLineupBindPlane(Model):
    pass


class SetWaypointIgnoreLock(Model):
    reset: bool = False


class SetWaypointSafeZone(Model):
    is_reset: bool = False
    margin_left: typing.Literal[0]
    margin_right: typing.Literal[0]
    margin_up: typing.Literal[0]
    margin_down: typing.Literal[0]


class ShowActivityPage(Model):
    panel_id: list[int]


class ShowBillboardInStoryMode(Model):
    target_type: target.Target
    is_show: bool = False


class ShowDeleteMissionDialog(Model):
    sub_mission_id: int
    on_all_completed: list["Task"]
    on_confirm: list["Task"]


class ShowEnvBuffDialog(Model):
    raid_id: int | None = None
    is_auto_get_param: bool = False
    on_cancel: list["Task"] | None = None


class ShowFistClubMissionPage(Model):
    fist_index: int | None = None
    on_page_cancel: list["Task"]


class ShowFuncBtn(Model):
    class PuzzleFunc(enum.Enum):
        Identify = "Identify"
        Match7thGuessTheSilhouette = "Match7thGuessTheSilhouette"
        SpecialVision = "SpecialVision"
        SpecialVisionFindSneakMonster = "SpecialVisionFindSneakMonster"
        TriggerCustomString = "TriggerCustomString"

    hide_when_graph_finish: bool = True
    show: bool = True
    item_id: int | None = None
    puzzle_func: PuzzleFunc | None = None
    c_d_duration: float | None = None
    show_btn_fuc_hint: bool = True
    custom_string: Value[str] | None = None
    show_btn_effect: bool = False
    override_btn_hint: Text | None = None
    override_icon_path: str | None = None
    mission_id: FixedValue[int] | Dynamic | None = None


class ShowGroupChallengeSelectPage(Model):
    pass


class ShowGuideHintWithText(Model):
    block: bool = False
    target_event: list["Task"]
    node_id_list: list[str]
    is_auto_match_guide_hint_type: bool = True
    guide_hint_type: input.GuideHintType | None = None
    guide_text_type: input.GuideTextType | None = None
    guide_text: str | None = None
    guide_text_p_c: typing.Literal["TutorialTextmap_401202"] | None = None
    guide_talk_id: int | None = None
    guide_text_controller: str | None = None
    override_action_name: input.ActionName | None = None
    show_key_map_tip: bool = True
    custom_text_direction: input.Direction | None = None
    guide_hint_show_config: input.ShowConfig | None = None
    guide_text_show_config: input.ShowConfig | None = None
    guide_ui_context_config: input.ContextConfig | None = None
    enable_navigation: bool = False
    enable_submit: bool = False
    enable_click_in_hint_area: bool = False
    enable_action_list: list[str] | None = None
    enable_battle_operation_list: list[str] | None = None
    param_int: Dynamic | None = None
    show_delay: float | None = None
    disable_black_mask: bool = False
    task_enabled: bool = True


class ShowGuideText(Model):
    class TextPath(enum.Enum):
        Contents_Text = "Contexts/Text"
        ContextsText = "ContextsText"
        Text = "Text"

    class PCGuide(BaseModel):
        use_pc_guide: typing.Annotated[bool, pydantic.Field(alias="UsePCGuide")] = False
        guide_res_id: int | None = None
        path: pathlib.Path | None = None
        text_path: "ShowGuideText.TextPath | None" = None
        text: str | None = None
        controller_text: str | None = None
        action_name: str | None = None
        controller_action_name: str | None = None
        copy_anchor_and_sale: bool = False
        offset_x: int | None = None
        offset_y: int | None = None

    id: int
    guide_res_id: int | None = None
    node_id: str | None = None
    path: str | None = None
    show: bool = False
    text_path: TextPath | None = None
    text: str | None = None
    action_name: str | None = None
    copy_anchor_and_sale: bool = False
    follow: bool = True
    is_3_d_object: bool = False
    offset_x: int | None = None
    offset_y: int | None = None
    pc_guide: typing.Annotated[PCGuide, pydantic.Field(alias="PCGuide")]
    task_enabled: bool = True


class ShowHeartDialToast(Model):
    step_type: typing.Literal["Lock", "Normal"]
    target_type: target.Target


class ShowMazeUI(Model):
    is_show: bool = False
    task_enabled: bool = True


class ShowMuseumPage(Model):
    auto_open_game_play_ui: bool = False


class ShowOfferingClockieUpgradeHint(Model):
    offering_type_id: typing.Literal[1]
    phase_id: int


class ShowPerformanceRollingSubtitles(Model):
    prev_duration: float | None = None
    json_config: pathlib.Path


class ShowPlayGOSubPackageDialog(Model):
    pass


class ShowRogueTalkBg(Model):
    talk_bg_id: int


class ShowReading(Model):
    book_id: FixedValue[int]
    should_pause_game: bool = False


class ShowRogueTalkUI(Model):
    show: bool


class ShowSDFText(Model):
    is_show: bool = False
    target_type: target.Target
    is_face_to_camera: FixedValue[int]
    sdf_text_id: typing.Annotated[Dynamic | None, pydantic.Field(alias="SDFTextID")] = None
    sdf_text_effect: typing.Annotated[Dynamic | None, pydantic.Field(alias="SDFTextID")] = None
    animator_param: Dynamic | None = None
    font_size: Dynamic | None = None
    is_set_scale: Dynamic | None = None
    dense_type_scale: Dynamic | None = None
    tall_type_scale: Dynamic | None = None
    english_like_scale: Dynamic | None = None


class ShowShop(Model):
    disable_bought_hint: bool = False
    shop_type: int
    task_id: list[None] | None


class ShowSpaceZooMainPage(Model):
    page_type: typing.Literal["Bag", "Cattery", "Main"]
    on_ui_enter: list["Task"] | None = None


class ShowSubPackage(Model):
    pass


class ShowTalkUI(Model):
    show: bool = False
    show_dialog_control_ui: bool = True
    task_enabled: bool = True


class ShowTransitionLoadingUI(Model):
    name: str


class ShowTutorialGuide(Model):
    guide_id: int
    wait_for_exit: bool = False
    task_enabled: bool = True


class ShowTutorialUI(Model):
    is_hide: bool = False
    associated_ui_name: str | None = None
    force_show_dialog: bool = False
    task_enabled: bool = True


class ShowUI(Model):
    name: str
    wait_for_exit: bool = False
    param: Value[str] | None = None
    on_ui_custom_event: list[None] | None = None
    on_ui_exit_immediately: list["Task"] | None = None
    on_ui_enter: list["Task"] | None = None
    task_enabled: bool = True


class ShowWaypointByProp(Model):
    target_type: target.Target | None = None
    use_owner_entity: bool = False
    group_id: FixedValue[int] | Dynamic | None = None
    instance_id: FixedValue[int] | Dynamic | None = None
    min_range: int | None = None
    prop_key: Custom | None = None
    max_range: int | None = None
    icon_path: str | None = None
    offset: Axis | None = None
    on_name_board: bool = False
    task_enabled: bool = True


class ShowWorldShop(Model):
    shop_type: int
    shop_id: int


class ShowWorldShop4ThUpgradeHint(Model):
    offering_type_id: typing.Literal[6]
    phase_id: int


class SpeedLineEffect(Model):
    active: bool = True
    speed: float
    divide: float
    start: float
    brightness: float
    density: float
    speedline_seed_path: str


class StartDialogueEntityInteract(Model):
    target_type: target.Target | None = None
    level_graph_path: pathlib.Path
    use_override_data: bool = False
    value_source: value.ValueSource
    override_tasks: camera.OverrideTasks | None = None


class StartPropInteractMode(Model):
    class Mode(enum.Enum):
        LockControl = "LockControl"
        OpenUI = "OpenUI"
        UseInteractiveProp = "UseInteractiveProp"
        UsePose01 = "UsePose01"
        UsePose02 = "UsePose02"

    class OverrideData01(BaseModel):
        areas_path: str
        area_name: str
        anchor_name: str

    target_type: target.Target
    mode: Mode | None = None
    use_override_data: bool = False
    override_data_0_1: OverrideData01 | None = None
    task_enabled: bool = True


class StopBlendShapesEmotion(Model):
    target_type: target.Target


class StopMunicipalChat(Model):
    municipal_chat_name: str


class StopPermanentEmotion(Model):
    target_type: target.Target


class StopRandomMissionTalk(Model):
    pass


class StoryLineReplaceTrialPlayer(Model):
    pass


class SwitchAudioListenerToTarget(Model):
    target_type: target.Target


class SwitchCase(Model):
    class SwitchCaseTask(BaseModel):
        predicate: predicate.Predicate
        success_task_list: list["Task"]

    task_list: list[SwitchCaseTask] | None = None
    default_task: list["Task"] | None = None


class SwitchCharacterAnchor(Model):
    is_local_player: bool = False
    character_unique_name: str | None = None
    area_name: Value[str] | Custom | None = None
    anchor_name: Value[str] | Custom | None = None
    reset_turn_in_place: bool = False
    target: Target | None = None
    attach_point: camera.AttachPoint | None = None
    reset_animation: bool = True
    reset_camera: bool = True


class SwitchCharacterAnchorV2(Model):
    switch_character_anchor_config: performance.SwitchCharacterAnchor
    task_enabled: bool = False


class SwitchPhotoGraphMode(Model):
    class PhotoGraphMode(enum.Enum):
        Identify = "Identify"
        IdentifyUAV = "IdentifyUAV"
        ShotUAV = "ShotUAV"

    photo_graph_mode: PhotoGraphMode | None = None
    skip_photo_preview_dialog: bool = False
    exit_when_pre_view_dialog_finish: bool = True
    identify_radius_override: FixedValue[int] | Dynamic | None = None
    identify_display_type: typing.Literal["March7thGuessTheSilhouette"] | None = None
    identify_max_exit_distance: typing.Literal[50] | None = None
    identify_look_at: target.Target | None = None
    init_fov: typing.Literal[1] | None = None
    task_enabled: bool = True


class SwitchUIMenuBGM(Model):
    should_stop: bool = False
    state_name: str | None = None


class SwordTrainingNotifySelectStory(Model):
    story_id: int


class TalkFigure(Model):
    show: bool = True
    image_path: str | None = None
    trigger_sound: bool = True
    task_enabled: bool = True


class TeleportToRotatableRegion(Model):
    target_region_index: FixedValue[int]
    target_anchor_group_id: FixedValue[int]
    target_anchor_instance_id: FixedValue[int]


class ToastPile(Model):
    img_path: str | None = None
    desc_text_id: Text | None = None
    desc_text_key: Value[str] | Custom | None = None
    task_enabled: bool = True


class TrainPartySwitchEnvironment(Model):
    name: typing.Literal["Train_Bar", "Train_Carriage", "Train_Default"]


class TransitEnvProfile(Model):
    path: Value[str] | Custom
    priority: typing.Literal["TASK_DYNAMIC_BLOCK_BATTLE_AREA"] | None = None
    duration: float | None = None


class TransitEnvProfileForStory(Model):
    path: Value[str]
    duration: float


class TriggerBattle(Model):
    event_id: FixedValue[int]
    group_id: FixedValue[int]
    battle_area_id: FixedValue[int]
    battle_area_config_id: FixedValue[int] | None = None


class TriggerBlendShapesEmotion(Model):
    target_type: target.Target
    emotion_name: str | None = None


class TriggerCustomString(Model):
    custom_string: Value[str] | Custom
    task_enabled: bool = True


class TriggerCustomStringList(Model):
    custom_string_list: list[str]


class TriggerCustomStringOnDialogEnd(Model):
    custom_string: Value[str]
    task_enabled: bool = True


class TriggerDialogueEvent(Model):
    dialogue_event_id: int


class TriggerDrinkMakerBartendInMainMission(Model):
    formula_id: int
    ingredient_ids: typing.Annotated[list[int], pydantic.Field(alias="IngredientIDs")]


class TriggerDrinkMakerBartendInMission(Model):
    request_id: int
    is_save_on_server: bool = False
    on_bartend_success: list["Task"]
    on_bartend_fail: list["Task"]


class TriggerEffect(Model):
    target_type: target.Target | None = None
    is_attach_to_target_entity: bool = False
    flags: list[typing.Literal["Field", "Resident"]]
    alive_only: bool = False
    effect_path: str
    param_entity_usage: typing.Literal["None"] | None = None
    position_offset: Axis | None = None
    unique_effect_name: str | None = None
    attach_point: camera.AttachPoint | None = None
    scale: Axis | None = None
    sub_object_modify_data_list: list[None] | None = None
    is_attach_to_caster: bool = False
    sync_prop_state: bool = False


class TriggerEffectList(Model):
    class Effect(BaseModel):
        effect_path: str
        is_attach_to_target_entity: bool = False
        attach_point: camera.AttachPoint | None = None
        position_offset: Axis | None = None
        scale: Axis | None = None
        sync_prop_state: bool = False

    target_type: target.Target | None = None
    effect_list: list[Effect]


class TriggerEffectOnAnchor(Model):
    area_name: str
    anchor_name: str
    effect_path: str


class TriggerEntityEvent(Model):
    event_name: Value[str]
    instance_id: FixedValue[int] | None = None


class TriggerEntityEventV2(Model):
    event_name: Value[str]
    target_type: target.Target | None = None


class TriggerGroupEvent(Model):
    event_name: Value[str]


class TriggerGroupEventOnDialogEnd(Model):
    event_name: Value[str]


class TriggerPerformance(Model):
    value_source: value.ValueSource | None = None
    performance_type: performance.Type | None = None
    performance_type_ds: typing.Annotated[Custom | None, pydantic.Field(alias="PerformanceType_DS")] = None
    performance_id: int
    performance_id_ds: typing.Annotated[Custom | None, pydantic.Field(alias="PerformanceID_DS")] = None
    save_progress: bool = False
    mask_config: performance.MaskConfig | None = None
    task_enabled: bool = True


class TriggerPermanentEmotion(Model):
    class EmotionName(enum.Enum):
        Angry01 = "Angry01"
        Close01 = "Close01"
        Close02 = "Close02"
        Close03 = "Close03"
        Happy01 = "Happy01"
        Proud01 = "Proud01"
        Proud02 = "Proud02"
        Pround02 = "Pround02"
        Sad01 = "Sad01"
        Sad02 = "Sad02"
        Suprise01 = "Suprise01"
        Suprise02 = "Suprise02"
        Surprise01 = "Surprise01"
        Trouble01 = "Trouble01"
        Trouble02 = "Trouble02"

    emotion_name: EmotionName
    target_type: target.Target


class TriggerRogueDialogue(Model):
    dialogue_path: pathlib.Path


class TriggerSound(Model):
    sound_name: Value[str] | None = None
    unique_name: str | None = None
    emitter_type: typing.Literal["DefaultEmitter", "LocalPlayer", "NPC", "Prop", "TargetEvaluator"] | None = None
    target_type: target.Target | None = None
    group_id: int | None = None
    id: int | None = None
    is_prop_lod_loop: bool = False
    event_cd: typing.Annotated[int | None, pydantic.Field(alias="EventCD")] = None
    task_enabled: bool = True


class TriggerUINotify(Model):
    notify_type_name: str


class TutorialTaskUnlock(Model):
    trigger_param: Value[str]


class UnLockPlayerControl(Model):
    un_lock_camera_control: bool = True


class UpdateTreasureChallengeProgress(Model):
    raid_target_id: int | None
    is_increase: bool
    delta_value: int


class VCameraConfigChange(Model):
    character_camera_target_type: target.Target | None = None
    camera_config: camera.CameraConfig | camera.CameraFreelook3rdConfig | camera.CameraShakeConfig
    task_enabled: bool = False


class VerifyInteractingEntity(Model):
    is_dialogue_target: bool = False
    is_owner_entity: bool = False
    group_id: int | None = None
    config_id: int | None = None


class WaitCustomString(Model):
    custom_string: Value[str] | Custom | None = None
    wait_owner_only: bool = False
    go_next_immediately: bool = False
    reset_when_task_begin: bool = False
    task_enabled: bool = True


class WaitDialogueEvent(Model):
    dialogue_event_list: list[talk.DialogueEvent]


class WaitFloorCustomValueChange(Model):
    name: Value[str]
    on_change: list["Task"]
    condition: predicate.Predicate | None = None
    is_loop: bool = True


class WaitFloorCustomValueChangeV2(Model):
    name: Value[str] | Custom
    on_change: list["Task"]
    condition: predicate.Predicate | None = None


class WaitFloorSavedValueChangeV2(Model):
    name: Value[str] | None = None
    condition: predicate.Predicate | None = None
    on_change: list["Task"]
    is_loop: bool = True


class WaitFor(Model):
    predicate: predicate.Predicate


class WaitFrame(Model):
    wait_frame_count: int | None = None
    task_enabled: bool = True


class WaitGroupEvent(Model):
    event_name: Value[str]
    on_event: list["Task"] | None = None
    is_loop: bool = True
    task_enabled: bool = False


class WaitMissionCustomValueChange(Model):
    main_mission_id: int | None = None
    mission_custom_value: mission.MissionCustomValue | None = None
    on_change: list["Task"]
    condition: predicate.Predicate | None = None
    task_enabled: bool = True


class WaitMissionTalkFinish(Model):
    task_enabled: bool = True


class WaitNewDecalDialogExit(Model):
    wait_decal_list: list[typing.Literal[9]]


class WaitPerformanceEnd(Model):
    pass


class WaitPhotoGraphResult(Model):
    wait_photo_result: list[str]
    complete_match: bool = False
    on_success: list["Task"]
    on_fail: list["Task"] | None = None
    is_loop: bool = True


class WaitPredicateSucc(Model):
    pass


class WaitPropDestroy(Model):
    on_success: list["Task"]
    target_type: target.Target


class WaitRogueSimpleTalkFinish(Model):
    pass


class WaitSecond(Model):
    wait_time: FixedValue[float] | Dynamic | None = None
    max_advence_per_tick: float | None = None
    is_realtime: bool = False
    task_enabled: bool = False


class WaitSilverWolfCompanionToastExit(Model):
    mission_id: int
    avatar_id: int
    max_wait_time: int


class WaitSimpleTalkFinish(Model):
    pass


class WaitStreamingJobFinished(Model):
    stop_loading_tick: bool = False


class WaitTutorial(Model):
    event: str
    param: str | None = None
    task_enabled: bool = True
    go_next_immediately: bool = False
    on_success_immediate: list["Task"] | None = None
    block_on_waiting: bool = False


class WaitUIControllerClose(Model):
    ui_controller_name: str | None = None


class WaitUIEvent(Model):
    ui_event_type: typing.Literal["FindTrotter"]


class WaitUINodeOpen(Model):
    node_id: str | None = None
    path: str | None = None
    skip_check: bool = False
    reverse: bool = False


# 因为太大了导致 Pyright 无法继续分析，所以按首字母拆一下
__TaskA = (
    typing.Annotated[ActiveTemplateVirtualCamera, pydantic.Tag("ActiveTemplateVirtualCamera")]
    | typing.Annotated[ActiveVirtualCamera, pydantic.Tag("ActiveVirtualCamera")]
    | typing.Annotated[
        ActiveVirtualCamera_PerformanceTransition, pydantic.Tag("ActiveVirtualCamera_PerformanceTransition")
    ]
    | typing.Annotated[AddFinishMissionData_ConsumeItem, pydantic.Tag("AddFinishMissionData_ConsumeItem")]
    | typing.Annotated[AddFinishMissionData_SelectConsumeItem, pydantic.Tag("AddFinishMissionData_SelectConsumeItem")]
    | typing.Annotated[AddFinishMissionData_PlayMessage, pydantic.Tag("AddFinishMissionData_PlayMessage")]
    | typing.Annotated[AddStreamingSource, pydantic.Tag("AddStreamingSource")]
    | typing.Annotated[AddTrialPlayer, pydantic.Tag("AddTrialPlayer")]
    | typing.Annotated[AdvAINavigateTo, pydantic.Tag("AdvAINavigateTo")]
    | typing.Annotated[AdvCharacterDisableHitBox, pydantic.Tag("AdvCharacterDisableHitBox")]
    | typing.Annotated[AdvClientChangePropState, pydantic.Tag("AdvClientChangePropState")]
    | typing.Annotated[AdvCreateEntityAsync, pydantic.Tag("AdvCreateEntityAsync")]
    | typing.Annotated[AdvCreateGroupEntity, pydantic.Tag("AdvCreateGroupEntity")]
    | typing.Annotated[AdvCreateGroupEntityV2, pydantic.Tag("AdvCreateGroupEntityV2")]
    | typing.Annotated[AdvDestroyEntityAsync, pydantic.Tag("AdvDestroyEntityAsync")]
    | typing.Annotated[AdvDestroyGroupEntity, pydantic.Tag("AdvDestroyGroupEntity")]
    | typing.Annotated[AdvEnablePropDialogMode, pydantic.Tag("AdvEnablePropDialogMode")]
    | typing.Annotated[AdvEntityFaceTo, pydantic.Tag("AdvEntityFaceTo")]
    | typing.Annotated[AdvEntityFaceToPoint, pydantic.Tag("AdvEntityFaceToPoint")]
    | typing.Annotated[AdvEntityStopLookAt, pydantic.Tag("AdvEntityStopLookAt")]
    | typing.Annotated[AdventureCameraLookAt, pydantic.Tag("AdventureCameraLookAt")]
    | typing.Annotated[AdventureCameraLookAtSimple, pydantic.Tag("AdventureCameraLookAtSimple")]
    | typing.Annotated[AdventureForbidAttackTriggerBattle, pydantic.Tag("AdventureForbidAttackTriggerBattle")]
    | typing.Annotated[AdventureShowReading, pydantic.Tag("AdventureShowReading")]
    | typing.Annotated[AdvHideMazeBtn, pydantic.Tag("AdvHideMazeBtn")]
    | typing.Annotated[AdvNpcFaceTo, pydantic.Tag("AdvNpcFaceTo")]
    | typing.Annotated[AdvNpcFaceToPlayer, pydantic.Tag("AdvNpcFaceToPlayer")]
    | typing.Annotated[AdvSetAIFollow, pydantic.Tag("AdvSetAIFollow")]
    | typing.Annotated[AdvSpecialVisionProtect, pydantic.Tag("AdvSpecialVisionProtect")]
    | typing.Annotated[AnimSetParameter, pydantic.Tag("AnimSetParameter")]
)

__TaskB = (
    typing.Annotated[BattlePerformInit, pydantic.Tag("BattlePerformInit")]
    | typing.Annotated[BattlePerformTimeline, pydantic.Tag("BattlePerformTimeline")]
    | typing.Annotated[BattlePlayVideo, pydantic.Tag("BattlePlayVideo")]
    | typing.Annotated[BlockInputController, pydantic.Tag("BlockInputController")]
    | typing.Annotated[ByHeroGender, pydantic.Tag("ByHeroGender")]
)

__TaskC = (
    typing.Annotated[CacheUI, pydantic.Tag("CacheUI")]
    | typing.Annotated[CalculateMissionCustomValue, pydantic.Tag("CalculateMissionCustomValue")]
    | typing.Annotated[CaptureLocalPlayer, pydantic.Tag("CaptureLocalPlayer")]
    | typing.Annotated[CaptureNPCToCharacter, pydantic.Tag("CaptureNPCToCharacter")]
    | typing.Annotated[ChangeDynamicOptionalBlock, pydantic.Tag("ChangeDynamicOptionalBlock")]
    | typing.Annotated[ChangeHeartDialModelByScript, pydantic.Tag("ChangeHeartDialModelByScript")]
    | typing.Annotated[ChangeHeroType, pydantic.Tag("ChangeHeroType")]
    | typing.Annotated[ChangePropState, pydantic.Tag("ChangePropState")]
    | typing.Annotated[ChangeTeamLeader, pydantic.Tag("ChangeTeamLeader")]
    | typing.Annotated[ChangeTrackingMission, pydantic.Tag("ChangeTrackingMission")]
    | typing.Annotated[ChangeTrackVirtualCameraFollowAndAim, pydantic.Tag("ChangeTrackVirtualCameraFollowAndAim")]
    | typing.Annotated[CharacterDisableLookAt, pydantic.Tag("CharacterDisableLookAt")]
    | typing.Annotated[CharacterHeadLookAt, pydantic.Tag("CharacterHeadLookAt")]
    | typing.Annotated[CharacterHeadStopLookAt, pydantic.Tag("CharacterHeadStopLookAt")]
    | typing.Annotated[CharacterNavigateTo, pydantic.Tag("CharacterNavigateTo")]
    | typing.Annotated[CharacterSteerTo, pydantic.Tag("CharacterSteerTo")]
    | typing.Annotated[CharacterStopFreeStyle, pydantic.Tag("CharacterStopFreeStyle")]
    | typing.Annotated[CharacterTriggerAnimState, pydantic.Tag("CharacterTriggerAnimState")]
    | typing.Annotated[CharacterTriggerFreeStyle, pydantic.Tag("CharacterTriggerFreeStyle")]
    | typing.Annotated[CharacterTriggerFreeStyleGraph, pydantic.Tag("CharacterTriggerFreeStyleGraph")]
    | typing.Annotated[
        CheckMainMissionFinishedInCurrentVersion, pydantic.Tag("CheckMainMissionFinishedInCurrentVersion")
    ]
    | typing.Annotated[ClearDialogCamera, pydantic.Tag("ClearDialogCamera")]
    | typing.Annotated[ClearNpcDistanceTrigger, pydantic.Tag("ClearNpcDistanceTrigger")]
    | typing.Annotated[ClearTalkUI, pydantic.Tag("ClearTalkUI")]
    | typing.Annotated[ClientFinishMission, pydantic.Tag("ClientFinishMission")]
    | typing.Annotated[ClosePage, pydantic.Tag("ClosePage")]
    | typing.Annotated[CollectDataConditions, pydantic.Tag("CollectDataConditions")]
    | typing.Annotated[ConsumeMissionItem, pydantic.Tag("ConsumeMissionItem")]
    | typing.Annotated[ConsumeMissionItemPerformance, pydantic.Tag("ConsumeMissionItemPerformance")]
    | typing.Annotated[ConsumeOrigamiItem, pydantic.Tag("ConsumeOrigamiItem")]
    | typing.Annotated[ConvinceInitialize, pydantic.Tag("ConvinceInitialize")]
    | typing.Annotated[ConvinceMoveCurrTurnOption, pydantic.Tag("ConvinceMoveCurrTurnOption")]
    | typing.Annotated[ConvinceMoveNextTurn, pydantic.Tag("ConvinceMoveNextTurn")]
    | typing.Annotated[ConvinceMovePrevTurn, pydantic.Tag("ConvinceMovePrevTurn")]
    | typing.Annotated[ConvinceMoveTurn, pydantic.Tag("ConvinceMoveTurn")]
    | typing.Annotated[ConvincePlayOptionTalk, pydantic.Tag("ConvincePlayOptionTalk")]
    | typing.Annotated[ConvinceShowToast, pydantic.Tag("ConvinceShowToast")]
    | typing.Annotated[ConvinceWaitAllTurnFinish, pydantic.Tag("ConvinceWaitAllTurnFinish")]
    | typing.Annotated[ConvinceWaitTrickSkill, pydantic.Tag("ConvinceWaitTrickSkill")]
    | typing.Annotated[ConvinceWaitTurnBegin, pydantic.Tag("ConvinceWaitTurnBegin")]
    | typing.Annotated[CreateAirline, pydantic.Tag("CreateAirline")]
    | typing.Annotated[CreateLevelAreas, pydantic.Tag("CreateLevelAreas")]
    | typing.Annotated[CreateNPC, pydantic.Tag("CreateNPC")]
    | typing.Annotated[CreatePhoneOnCharacter, pydantic.Tag("CreatePhoneOnCharacter")]
    | typing.Annotated[CreateProp, pydantic.Tag("CreateProp")]
    | typing.Annotated[CreateTrialPlayer, pydantic.Tag("CreateTrialPlayer")]
)

__TaskD = (
    typing.Annotated[DebateInitialize, pydantic.Tag("DebateInitialize")]
    | typing.Annotated[DebateReturnTestimony, pydantic.Tag("DebateReturnTestimony")]
    | typing.Annotated[DebateShowToast, pydantic.Tag("DebateShowToast")]
    | typing.Annotated[DestroyCurvePropGroupPuzzle, pydantic.Tag("DestroyCurvePropGroupPuzzle")]
    | typing.Annotated[DestroyNPC, pydantic.Tag("DestroyNPC")]
    | typing.Annotated[DestroyProp, pydantic.Tag("DestroyProp")]
    | typing.Annotated[DestroyTrialPlayer, pydantic.Tag("DestroyTrialPlayer")]
)

__TaskE = (
    typing.Annotated[EnableBillboard, pydantic.Tag("EnableBillboard")]
    | typing.Annotated[EnableNPCMonsterAI, pydantic.Tag("EnableNPCMonsterAI")]
    | typing.Annotated[EnablePerformanceMode, pydantic.Tag("EnablePerformanceMode")]
    | typing.Annotated[EndDialogueEntityInteract, pydantic.Tag("EndDialogueEntityInteract")]
    | typing.Annotated[EndPerformance, pydantic.Tag("EndPerformance")]
    | typing.Annotated[EndPropInteract, pydantic.Tag("EndPropInteract")]
    | typing.Annotated[EnterFlipperLightDeviceControl, pydantic.Tag("EnterFlipperLightDeviceControl")]
    | typing.Annotated[EnterMap, pydantic.Tag("EnterMap")]
    | typing.Annotated[EnterMapByCondition, pydantic.Tag("EnterMapByCondition")]
    | typing.Annotated[ExitTransitionLoadingUI, pydantic.Tag("ExitTransitionLoadingUI")]
)

__TaskF = (
    typing.Annotated[FinishLevelGraph, pydantic.Tag("FinishLevelGraph")]
    | typing.Annotated[FinishPerformanceMission, pydantic.Tag("FinishPerformanceMission")]
    | typing.Annotated[FinishRogueAeonTalk, pydantic.Tag("FinishRogueAeonTalk")]
    | typing.Annotated[ForceSetDialogCamera, pydantic.Tag("ForceSetDialogCamera")]
)

__TaskG = typing.Annotated[GuessTheSilhouetteResult, pydantic.Tag("GuessTheSilhouetteResult")]

__TaskH = (
    typing.Annotated[HeliobusSNSQuickPost, pydantic.Tag("HeliobusSNSQuickPost")]
    | typing.Annotated[HideAllEntity, pydantic.Tag("HideAllEntity")]
    | typing.Annotated[HideEntity, pydantic.Tag("HideEntity")]
    | typing.Annotated[HideEntityV2, pydantic.Tag("HideEntityV2")]
    | typing.Annotated[HideSummonUnit, pydantic.Tag("HideSummonUnit")]
    | typing.Annotated[HideTopPage, pydantic.Tag("HideTopPage")]
    | typing.Annotated[HideWaypointByProp, pydantic.Tag("HideWaypointByProp")]
)

__TaskL = (
    typing.Annotated[LensDistortionCurveEffect, pydantic.Tag("LensDistortionCurveEffect")]
    | typing.Annotated[LevelAudioState, pydantic.Tag("LevelAudioState")]
    | typing.Annotated[LevelPerformanceInitialize, pydantic.Tag("LevelPerformanceInitialize")]
    | typing.Annotated[LockCurrentTeleportAction, pydantic.Tag("LockCurrentTeleportAction")]
    | typing.Annotated[LockPhotoIdentifyHint, pydantic.Tag("LockPhotoIdentifyHint")]
    | typing.Annotated[LockPlayerControl, pydantic.Tag("LockPlayerControl")]
    | typing.Annotated[LockTeamLeader, pydantic.Tag("LockTeamLeader")]
)

__TaskM = (
    typing.Annotated[MonsterResearchSubmit, pydantic.Tag("MonsterResearchSubmit")]
    | typing.Annotated[MoveVirtualCameraOnDollyPath, pydantic.Tag("MoveVirtualCameraOnDollyPath")]
)

__TaskN = (
    typing.Annotated[NpcPossession, pydantic.Tag("NpcPossession")]
    | typing.Annotated[NpcSetupTrigger, pydantic.Tag("NpcSetupTrigger")]
    | typing.Annotated[NpcToPlayerDistanceTrigger, pydantic.Tag("NpcToPlayerDistanceTrigger")]
)

__TaskO = (
    typing.Annotated[OnMuseumPerformanceBegin, pydantic.Tag("OnMuseumPerformanceBegin")]
    | typing.Annotated[OnMuseumPerformanceEnd, pydantic.Tag("OnMuseumPerformanceEnd")]
    | typing.Annotated[OpenRaid, pydantic.Tag("OpenRaid")]
    | typing.Annotated[OpenTreasureChallenge, pydantic.Tag("OpenTreasureChallenge")]
    | typing.Annotated[OverrideEndTransferColor, pydantic.Tag("OverrideEndTransferColor")]
    | typing.Annotated[OverrideEndTransferType, pydantic.Tag("OverrideEndTransferType")]
    | typing.Annotated[OverrideFinishActionAutoTransfer, pydantic.Tag("OverrideFinishActionAutoTransfer")]
    | typing.Annotated[OverridePerformanceEndCrack, pydantic.Tag("OverridePerformanceEndCrack")]
)

__TaskP = (
    typing.Annotated[PerformanceEndBlackText, pydantic.Tag("PerformanceEndBlackText")]
    | typing.Annotated[PerformanceEndSeq, pydantic.Tag("PerformanceEndSeq")]
    | typing.Annotated[PerformanceExtendEndBlack, pydantic.Tag("PerformanceExtendEndBlack")]
    | typing.Annotated[PerformanceTransition, pydantic.Tag("PerformanceTransition")]
    | typing.Annotated[PhotoGraphAimTarget, pydantic.Tag("PhotoGraphAimTarget")]
    | typing.Annotated[PhotoGraphShowIdentifyResult, pydantic.Tag("PhotoGraphShowIdentifyResult")]
    | typing.Annotated[PhotoGraphWaitIdentifyFinish, pydantic.Tag("PhotoGraphWaitIdentifyFinish")]
    | typing.Annotated[PlayAeonTalk, pydantic.Tag("PlayAeonTalk")]
    | typing.Annotated[PlayAndWaitRogueSimpleTalk, pydantic.Tag("PlayAndWaitRogueSimpleTalk")]
    | typing.Annotated[PlayAndWaitSimpleTalk, pydantic.Tag("PlayAndWaitSimpleTalk")]
    | typing.Annotated[PlayerForceWalk, pydantic.Tag("PlayerForceWalk")]
    | typing.Annotated[PlayerRemoteControlOtherEntity, pydantic.Tag("PlayerRemoteControlOtherEntity")]
    | typing.Annotated[PlayerSelectMotionMode, pydantic.Tag("PlayerSelectMotionMode")]
    | typing.Annotated[PlayFullScreenTransfer, pydantic.Tag("PlayFullScreenTransfer")]
    | typing.Annotated[PlayNPCBubbleTalk, pydantic.Tag("PlayNPCBubbleTalk")]
    | typing.Annotated[PlayNPCSingleBubbleTalk, pydantic.Tag("PlayNPCSingleBubbleTalk")]
    | typing.Annotated[PlayMazeButtonEffect, pydantic.Tag("PlayMazeButtonEffect")]
    | typing.Annotated[PlayMessage, pydantic.Tag("PlayMessage")]
    | typing.Annotated[PlayMissionTalk, pydantic.Tag("PlayMissionTalk")]
    | typing.Annotated[PlayMultiVoiceTalk, pydantic.Tag("PlayMultiVoiceTalk")]
    | typing.Annotated[PlayMunicipalChat, pydantic.Tag("PlayMunicipalChat")]
    | typing.Annotated[PlayOptionTalk, pydantic.Tag("PlayOptionTalk")]
    | typing.Annotated[PlayOrigamiTraceTalk, pydantic.Tag("PlayOrigamiTraceTalk")]
    | typing.Annotated[PlayRogueOptionTalk, pydantic.Tag("PlayRogueOptionTalk")]
    | typing.Annotated[PlayRogueSimpleTalk, pydantic.Tag("PlayRogueSimpleTalk")]
    | typing.Annotated[PlaySimpleTalk, pydantic.Tag("PlaySimpleTalk")]
    | typing.Annotated[PlayScreenCrack, pydantic.Tag("PlayScreenCrack")]
    | typing.Annotated[PlayScreenTransfer, pydantic.Tag("PlayScreenTransfer")]
    | typing.Annotated[PlaySequenceDialogue, pydantic.Tag("PlaySequenceDialogue")]
    | typing.Annotated[PlayTimeline, pydantic.Tag("PlayTimeline")]
    | typing.Annotated[PlayTimelinePrefab, pydantic.Tag("PlayTimelinePrefab")]
    | typing.Annotated[PlayVideo, pydantic.Tag("PlayVideo")]
    | typing.Annotated[PlayVoice, pydantic.Tag("PlayVoice")]
    | typing.Annotated[PlayVoice_Sequence, pydantic.Tag("PlayVoice_Sequence")]
    | typing.Annotated[PPFilterStackEffect, pydantic.Tag("PPFilterStackEffect")]
    | typing.Annotated[PredicateTaskList, pydantic.Tag("PredicateTaskList")]
    | typing.Annotated[PredicateTaskListWithFail, pydantic.Tag("PredicateTaskListWithFail")]
    | typing.Annotated[PropDestruct, pydantic.Tag("PropDestruct")]
    | typing.Annotated[PropEnableCollider, pydantic.Tag("PropEnableCollider")]
    | typing.Annotated[PropMoveTo, pydantic.Tag("PropMoveTo")]
    | typing.Annotated[PropReqInteract, pydantic.Tag("PropReqInteract")]
    | typing.Annotated[PropSetupHitBox, pydantic.Tag("PropSetupHitBox")]
    | typing.Annotated[PropSetupTrigger, pydantic.Tag("PropSetupTrigger")]
    | typing.Annotated[PropSetupUITrigger, pydantic.Tag("PropSetupUITrigger")]
    | typing.Annotated[PropSetVisibility, pydantic.Tag("PropSetVisibility")]
    | typing.Annotated[PropStateChangeListenerConfig, pydantic.Tag("PropStateChangeListenerConfig")]
    | typing.Annotated[PropStateExecute, pydantic.Tag("PropStateExecute")]
    | typing.Annotated[PropTriggerAnimState, pydantic.Tag("PropTriggerAnimState")]
    | typing.Annotated[PuzzleSetAnimatorParams, pydantic.Tag("PuzzleSetAnimatorParams")]
)

__TaskQ = typing.Annotated[QuestGetReward, pydantic.Tag("QuestGetReward")]

__TaskR = (
    typing.Annotated[RadialBlurEffect, pydantic.Tag("RadialBlurEffect")]
    | typing.Annotated[RaidSceneTransfer, pydantic.Tag("RaidSceneTransfer")]
    | typing.Annotated[RandomConfig, pydantic.Tag("RandomConfig")]
    | typing.Annotated[ReleaseCacheUI, pydantic.Tag("ReleaseCacheUI")]
    | typing.Annotated[ReleaseCharacter, pydantic.Tag("ReleaseCharacter")]
    | typing.Annotated[ReleaseEnvProfileForStory, pydantic.Tag("ReleaseEnvProfileForStory")]
    | typing.Annotated[RemoveAirline, pydantic.Tag("RemoveAirline")]
    | typing.Annotated[RemoveBattleEventData, pydantic.Tag("RemoveBattleEventData")]
    | typing.Annotated[RemoveEffect, pydantic.Tag("RemoveEffect")]
    | typing.Annotated[RemoveLevelAreas, pydantic.Tag("RemoveLevelAreas")]
    | typing.Annotated[RemoveMazeBuff, pydantic.Tag("RemoveMazeBuff")]
    | typing.Annotated[RemoveStreamingSource, pydantic.Tag("RemoveStreamingSource")]
    | typing.Annotated[RemoveVirtualLineupBindPlane, pydantic.Tag("RemoveVirtualLineupBindPlane")]
    | typing.Annotated[ReplaceTrialPlayer, pydantic.Tag("ReplaceTrialPlayer")]
    | typing.Annotated[ReplaceVirtualTeam, pydantic.Tag("ReplaceVirtualTeam")]
    | typing.Annotated[ResetBillboardInfo, pydantic.Tag("ResetBillboardInfo")]
    | typing.Annotated[ResetMissionAudioState, pydantic.Tag("ResetMissionAudioState")]
    | typing.Annotated[ResetMissionWayPoint, pydantic.Tag("ResetMissionWayPoint")]
    | typing.Annotated[ResetPhotoGraphTargets, pydantic.Tag("ResetPhotoGraphTargets")]
    | typing.Annotated[RestoreTrackingMission, pydantic.Tag("RestoreTrackingMission")]
    | typing.Annotated[RetrySwordTrainingFinalBattle, pydantic.Tag("RetrySwordTrainingFinalBattle")]
    | typing.Annotated[ReturnToLoginPage, pydantic.Tag("ReturnToLoginPage")]
    | typing.Annotated[RogueFinish, pydantic.Tag("RogueFinish")]
    | typing.Annotated[RogueShowSelectMainPage, pydantic.Tag("RogueShowSelectMainPage")]
)

__TaskS = (
    typing.Annotated[SaveMessage, pydantic.Tag("SaveMessage")]
    | typing.Annotated[SceneGachaListener, pydantic.Tag("SceneGachaListener")]
    | typing.Annotated[SelectMissionItem, pydantic.Tag("SelectMissionItem")]
    | typing.Annotated[SelectorConfig, pydantic.Tag("SelectorConfig")]
    | typing.Annotated[SequenceConfig, pydantic.Tag("SequenceConfig")]
    | typing.Annotated[SetAdvAchievement, pydantic.Tag("SetAdvAchievement")]
    | typing.Annotated[SetAllMissionWaypointsVisiable, pydantic.Tag("SetAllMissionWaypointsVisiable")]
    | typing.Annotated[SetAllRogueDoorState, pydantic.Tag("SetAllRogueDoorState")]
    | typing.Annotated[SetAsRogueDialogue, pydantic.Tag("SetAsRogueDialogue")]
    | typing.Annotated[SetAudioEmotionState, pydantic.Tag("SetAudioEmotionState")]
    | typing.Annotated[SetBattleBGMState, pydantic.Tag("SetBattleBGMState")]
    | typing.Annotated[SetBillboardInfo, pydantic.Tag("SetBillboardInfo")]
    | typing.Annotated[SetCharacterAtlasFaceEmotion, pydantic.Tag("SetCharacterAtlasFaceEmotion")]
    | typing.Annotated[SetCharacterShadowFactor, pydantic.Tag("SetCharacterShadowFactor")]
    | typing.Annotated[SetCharacterVisible, pydantic.Tag("SetCharacterVisible")]
    | typing.Annotated[SetClockBoyEmotion, pydantic.Tag("SetClockBoyEmotion")]
    | typing.Annotated[SetEffectAnimatorTrigger, pydantic.Tag("SetEffectAnimatorTrigger")]
    | typing.Annotated[SetEntityTalkEnable, pydantic.Tag("SetEntityTalkEnable")]
    | typing.Annotated[SetEntityVisible, pydantic.Tag("SetEntityVisible")]
    | typing.Annotated[SetFloorCustomBool, pydantic.Tag("SetFloorCustomBool")]
    | typing.Annotated[SetFloorCustomFloat, pydantic.Tag("SetFloorCustomFloat")]
    | typing.Annotated[SetFloorCustomFloatV2, pydantic.Tag("SetFloorCustomFloatV2")]
    | typing.Annotated[SetFloorCustomString, pydantic.Tag("SetFloorCustomString")]
    | typing.Annotated[SetFloorSavedValue, pydantic.Tag("SetFloorSavedValue")]
    | typing.Annotated[SetForceStreamingThisFrame, pydantic.Tag("SetForceStreamingThisFrame")]
    | typing.Annotated[SetFuncBtn, pydantic.Tag("SetFuncBtn")]
    | typing.Annotated[SetHLODSwitchDelay, pydantic.Tag("SetHLODSwitchDelay")]
    | typing.Annotated[SetHudTemplate, pydantic.Tag("SetHudTemplate")]
    | typing.Annotated[SetLoadingStratageType, pydantic.Tag("SetLoadingStratageType")]
    | typing.Annotated[SetLocalPlayerDitherAlpha, pydantic.Tag("SetLocalPlayerDitherAlpha")]
    | typing.Annotated[SetMissionAudioState, pydantic.Tag("SetMissionAudioState")]
    | typing.Annotated[SetMissionCustomValue, pydantic.Tag("SetMissionCustomValue")]
    | typing.Annotated[SetMissionWayPoint, pydantic.Tag("SetMissionWayPoint")]
    | typing.Annotated[SetMunicipalEnable, pydantic.Tag("SetMunicipalEnable")]
    | typing.Annotated[SetNPCMonstersVisible, pydantic.Tag("SetNPCMonstersVisible")]
    | typing.Annotated[SetNpcStatus, pydantic.Tag("SetNpcStatus")]
    | typing.Annotated[SetNpcWaypath, pydantic.Tag("SetNpcWaypath")]
    | typing.Annotated[SetPerformanceResult, pydantic.Tag("SetPerformanceResult")]
    | typing.Annotated[SetRogueRoomFinish, pydantic.Tag("SetRogueRoomFinish")]
    | typing.Annotated[SetSpecialVisionOn, pydantic.Tag("SetSpecialVisionOn")]
    | typing.Annotated[SetStageItemState, pydantic.Tag("SetStageItemState")]
    | typing.Annotated[SetTargetEntityFadeWithAnim, pydantic.Tag("SetTargetEntityFadeWithAnim")]
    | typing.Annotated[SetTargetUniqueName, pydantic.Tag("SetTargetUniqueName")]
    | typing.Annotated[SetTextJoinValue, pydantic.Tag("SetTextJoinValue")]
    | typing.Annotated[SetTraceOrigamiFlag, pydantic.Tag("SetTraceOrigamiFlag")]
    | typing.Annotated[SetTrackingMission, pydantic.Tag("SetTrackingMission")]
    | typing.Annotated[SetVirtualLineupBindPlane, pydantic.Tag("SetVirtualLineupBindPlane")]
    | typing.Annotated[SetWaypointIgnoreLock, pydantic.Tag("SetWaypointIgnoreLock")]
    | typing.Annotated[SetWaypointSafeZone, pydantic.Tag("SetWaypointSafeZone")]
    | typing.Annotated[ShowActivityPage, pydantic.Tag("ShowActivityPage")]
    | typing.Annotated[ShowBillboardInStoryMode, pydantic.Tag("ShowBillboardInStoryMode")]
    | typing.Annotated[ShowDeleteMissionDialog, pydantic.Tag("ShowDeleteMissionDialog")]
    | typing.Annotated[ShowEnvBuffDialog, pydantic.Tag("ShowEnvBuffDialog")]
    | typing.Annotated[ShowFistClubMissionPage, pydantic.Tag("ShowFistClubMissionPage")]
    | typing.Annotated[ShowFuncBtn, pydantic.Tag("ShowFuncBtn")]
    | typing.Annotated[ShowGroupChallengeSelectPage, pydantic.Tag("ShowGroupChallengeSelectPage")]
    | typing.Annotated[ShowGuideHintWithText, pydantic.Tag("ShowGuideHintWithText")]
    | typing.Annotated[ShowGuideText, pydantic.Tag("ShowGuideText")]
    | typing.Annotated[ShowHeartDialToast, pydantic.Tag("ShowHeartDialToast")]
    | typing.Annotated[ShowMazeUI, pydantic.Tag("ShowMazeUI")]
    | typing.Annotated[ShowMuseumPage, pydantic.Tag("ShowMuseumPage")]
    | typing.Annotated[ShowOfferingClockieUpgradeHint, pydantic.Tag("ShowOfferingClockieUpgradeHint")]
    | typing.Annotated[ShowPerformanceRollingSubtitles, pydantic.Tag("ShowPerformanceRollingSubtitles")]
    | typing.Annotated[ShowPlayGOSubPackageDialog, pydantic.Tag("ShowPlayGOSubPackageDialog")]
    | typing.Annotated[ShowRogueTalkBg, pydantic.Tag("ShowRogueTalkBg")]
    | typing.Annotated[ShowReading, pydantic.Tag("ShowReading")]
    | typing.Annotated[ShowRogueTalkUI, pydantic.Tag("ShowRogueTalkUI")]
    | typing.Annotated[ShowSDFText, pydantic.Tag("ShowSDFText")]
    | typing.Annotated[ShowShop, pydantic.Tag("ShowShop")]
    | typing.Annotated[ShowSpaceZooMainPage, pydantic.Tag("ShowSpaceZooMainPage")]
    | typing.Annotated[ShowSubPackage, pydantic.Tag("ShowSubPackage")]
    | typing.Annotated[ShowTalkUI, pydantic.Tag("ShowTalkUI")]
    | typing.Annotated[ShowTransitionLoadingUI, pydantic.Tag("ShowTransitionLoadingUI")]
    | typing.Annotated[ShowTutorialGuide, pydantic.Tag("ShowTutorialGuide")]
    | typing.Annotated[ShowTutorialUI, pydantic.Tag("ShowTutorialUI")]
    | typing.Annotated[ShowUI, pydantic.Tag("ShowUI")]
    | typing.Annotated[ShowWaypointByProp, pydantic.Tag("ShowWaypointByProp")]
    | typing.Annotated[ShowWorldShop, pydantic.Tag("ShowWorldShop")]
    | typing.Annotated[ShowWorldShop4ThUpgradeHint, pydantic.Tag("ShowWorldShop4ThUpgradeHint")]
    | typing.Annotated[SpeedLineEffect, pydantic.Tag("SpeedLineEffect")]
    | typing.Annotated[StartDialogueEntityInteract, pydantic.Tag("StartDialogueEntityInteract")]
    | typing.Annotated[StartPropInteractMode, pydantic.Tag("StartPropInteractMode")]
    | typing.Annotated[StopBlendShapesEmotion, pydantic.Tag("StopBlendShapesEmotion")]
    | typing.Annotated[StopMunicipalChat, pydantic.Tag("StopMunicipalChat")]
    | typing.Annotated[StopPermanentEmotion, pydantic.Tag("StopPermanentEmotion")]
    | typing.Annotated[StopRandomMissionTalk, pydantic.Tag("StopRandomMissionTalk")]
    | typing.Annotated[StoryLineReplaceTrialPlayer, pydantic.Tag("StoryLineReplaceTrialPlayer")]
    | typing.Annotated[SwitchAudioListenerToTarget, pydantic.Tag("SwitchAudioListenerToTarget")]
    | typing.Annotated[SwitchCase, pydantic.Tag("SwitchCase")]
    | typing.Annotated[SwitchCharacterAnchor, pydantic.Tag("SwitchCharacterAnchor")]
    | typing.Annotated[SwitchCharacterAnchorV2, pydantic.Tag("SwitchCharacterAnchorV2")]
    | typing.Annotated[SwitchPhotoGraphMode, pydantic.Tag("SwitchPhotoGraphMode")]
    | typing.Annotated[SwitchUIMenuBGM, pydantic.Tag("SwitchUIMenuBGM")]
    | typing.Annotated[SwordTrainingNotifySelectStory, pydantic.Tag("SwordTrainingNotifySelectStory")]
)

__TaskT = (
    typing.Annotated[TalkFigure, pydantic.Tag("TalkFigure")]
    | typing.Annotated[TeleportToRotatableRegion, pydantic.Tag("TeleportToRotatableRegion")]
    | typing.Annotated[ToastPile, pydantic.Tag("ToastPile")]
    | typing.Annotated[TrainPartySwitchEnvironment, pydantic.Tag("TrainPartySwitchEnvironment")]
    | typing.Annotated[TransitEnvProfile, pydantic.Tag("TransitEnvProfile")]
    | typing.Annotated[TransitEnvProfileForStory, pydantic.Tag("TransitEnvProfileForStory")]
    | typing.Annotated[TriggerBattle, pydantic.Tag("TriggerBattle")]
    | typing.Annotated[TriggerBlendShapesEmotion, pydantic.Tag("TriggerBlendShapesEmotion")]
    | typing.Annotated[TriggerCustomString, pydantic.Tag("TriggerCustomString")]
    | typing.Annotated[TriggerCustomStringList, pydantic.Tag("TriggerCustomStringList")]
    | typing.Annotated[TriggerCustomStringOnDialogEnd, pydantic.Tag("TriggerCustomStringOnDialogEnd")]
    | typing.Annotated[TriggerDialogueEvent, pydantic.Tag("TriggerDialogueEvent")]
    | typing.Annotated[TriggerDrinkMakerBartendInMainMission, pydantic.Tag("TriggerDrinkMakerBartendInMainMission")]
    | typing.Annotated[TriggerDrinkMakerBartendInMission, pydantic.Tag("TriggerDrinkMakerBartendInMission")]
    | typing.Annotated[TriggerEffect, pydantic.Tag("TriggerEffect")]
    | typing.Annotated[TriggerEffectList, pydantic.Tag("TriggerEffectList")]
    | typing.Annotated[TriggerEffectOnAnchor, pydantic.Tag("TriggerEffectOnAnchor")]
    | typing.Annotated[TriggerEntityEvent, pydantic.Tag("TriggerEntityEvent")]
    | typing.Annotated[TriggerEntityEventV2, pydantic.Tag("TriggerEntityEventV2")]
    | typing.Annotated[TriggerGroupEvent, pydantic.Tag("TriggerGroupEvent")]
    | typing.Annotated[TriggerGroupEventOnDialogEnd, pydantic.Tag("TriggerGroupEventOnDialogEnd")]
    | typing.Annotated[TriggerPerformance, pydantic.Tag("TriggerPerformance")]
    | typing.Annotated[TriggerPermanentEmotion, pydantic.Tag("TriggerPermanentEmotion")]
    | typing.Annotated[TriggerRogueDialogue, pydantic.Tag("TriggerRogueDialogue")]
    | typing.Annotated[TriggerSound, pydantic.Tag("TriggerSound")]
    | typing.Annotated[TriggerUINotify, pydantic.Tag("TriggerUINotify")]
    | typing.Annotated[TutorialTaskUnlock, pydantic.Tag("TutorialTaskUnlock")]
)

__TaskU = (
    typing.Annotated[UnLockPlayerControl, pydantic.Tag("UnLockPlayerControl")]
    | typing.Annotated[UpdateTreasureChallengeProgress, pydantic.Tag("UpdateTreasureChallengeProgress")]
)

__TaskV = (
    typing.Annotated[VCameraConfigChange, pydantic.Tag("VCameraConfigChange")]
    | typing.Annotated[VerifyInteractingEntity, pydantic.Tag("VerifyInteractingEntity")]
)

__TaskW = (
    typing.Annotated[WaitCustomString, pydantic.Tag("WaitCustomString")]
    | typing.Annotated[WaitDialogueEvent, pydantic.Tag("WaitDialogueEvent")]
    | typing.Annotated[WaitFloorCustomValueChange, pydantic.Tag("WaitFloorCustomValueChange")]
    | typing.Annotated[WaitFloorCustomValueChangeV2, pydantic.Tag("WaitFloorCustomValueChangeV2")]
    | typing.Annotated[WaitFloorSavedValueChangeV2, pydantic.Tag("WaitFloorSavedValueChangeV2")]
    | typing.Annotated[WaitFor, pydantic.Tag("WaitFor")]
    | typing.Annotated[WaitFrame, pydantic.Tag("WaitFrame")]
    | typing.Annotated[WaitGroupEvent, pydantic.Tag("WaitGroupEvent")]
    | typing.Annotated[WaitMissionCustomValueChange, pydantic.Tag("WaitMissionCustomValueChange")]
    | typing.Annotated[WaitMissionTalkFinish, pydantic.Tag("WaitMissionTalkFinish")]
    | typing.Annotated[WaitNewDecalDialogExit, pydantic.Tag("WaitNewDecalDialogExit")]
    | typing.Annotated[WaitPerformanceEnd, pydantic.Tag("WaitPerformanceEnd")]
    | typing.Annotated[WaitPhotoGraphResult, pydantic.Tag("WaitPhotoGraphResult")]
    | typing.Annotated[WaitPredicateSucc, pydantic.Tag("WaitPredicateSucc")]
    | typing.Annotated[WaitPropDestroy, pydantic.Tag("WaitPropDestroy")]
    | typing.Annotated[WaitRogueSimpleTalkFinish, pydantic.Tag("WaitRogueSimpleTalkFinish")]
    | typing.Annotated[WaitSecond, pydantic.Tag("WaitSecond")]
    | typing.Annotated[WaitSilverWolfCompanionToastExit, pydantic.Tag("WaitSilverWolfCompanionToastExit")]
    | typing.Annotated[WaitSimpleTalkFinish, pydantic.Tag("WaitSimpleTalkFinish")]
    | typing.Annotated[WaitStreamingJobFinished, pydantic.Tag("WaitStreamingJobFinished")]
    | typing.Annotated[WaitTutorial, pydantic.Tag("WaitTutorial")]
    | typing.Annotated[WaitUIControllerClose, pydantic.Tag("WaitUIControllerClose")]
    | typing.Annotated[WaitUIEvent, pydantic.Tag("WaitUIEvent")]
    | typing.Annotated[WaitUINodeOpen, pydantic.Tag("WaitUINodeOpen")]
)

Task = typing.Annotated[
    __TaskA
    | __TaskB
    | __TaskC
    | __TaskD
    | __TaskE
    | __TaskF
    | __TaskG
    | __TaskH
    | __TaskL
    | __TaskM
    | __TaskN
    | __TaskO
    | __TaskP
    | __TaskQ
    | __TaskR
    | __TaskS
    | __TaskT
    | __TaskU
    | __TaskV
    | __TaskW,
    pydantic.Discriminator(get_discriminator),
]
