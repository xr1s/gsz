"""这些结构体出现在 Config/Level/Mission/${MainMissionID} 下"""

import enum
import typing

import pydantic

from ...excel import item
from .base import BaseModel, Empty, Model, get_discriminator


class MissionActivePlaneType(enum.Enum):
    AllFloor = "AllFloor"
    SpecifiedPlaneType = "SpecifiedPlaneType"


class TakeType(enum.Enum):
    AnySequence = "AnySequence"
    Auto = "Auto"
    CustomValue = "CustomValue"
    MultiSequence = "MultiSequence"


class ParamType(enum.Enum):
    Equal = "Equal"
    EqualOrZeroAny = "EqualOrZeroAny"
    GreaterEqual = "GreaterEqual"
    IntContainListContain = "IntContainListContain"
    LessEqual = "LessEqual"
    ListContain = "ListContain"
    ListContainList = "ListContainList"
    NoPara = "NoPara"


class FinishActionType(enum.Enum):
    ActivateAnchor = "ActivateAnchor"
    ActivateGameplayCounter = "ActivateGameplayCounter"
    AddCustomValue = "AddCustomValue"
    AddMissionItem = "addMissionItem"
    AddRecoverMissionItem = "addRecoverMissionItem"
    ChangeLineup = "ChangeLineup"
    ChangeStoryLine = "ChangeStoryLine"
    DelMission = "delMission"
    DelMissionItem = "delMissionItem"
    DelSubMission = "delSubMission"
    DisableMission = "DisableMission"
    EnterEntryIfNotThere = "EnterEntryIfNotThere"
    MoveToAnchor = "MoveToAnchor"
    Recover = "Recover"
    SetCustomValue = "SetCustomValue"
    SetFloorSavedValue = "SetFloorSavedValue"
    SetGroupState = "SetGroupState"
    SetRaidValue = "SetRaidValue"


class FinishAction(BaseModel):
    finish_action_type: FinishActionType | None = None
    finish_action_para: list[int] | None = None
    finish_action_para_string: list[str] | None = None


class CustomValueReward(BaseModel):
    index: int | None = None
    value: int
    reward_id: int


class WayPointType(enum.Enum):
    Anchor = "Anchor"
    District = "District"
    Monster = "Monster"
    NPC = "NPC"
    Prop = "Prop"


class MissionCustomValue(BaseModel):
    index: int | None = None
    is_local: typing.Annotated[bool, pydantic.Field(alias="isLocal")] = False
    is_range: typing.Annotated[bool, pydantic.Field(alias="isRange")] = False
    valid_value_param_list: list[int] | None = None


class MultiPhaseWaypoint(BaseModel):
    mission_custom_value: MissionCustomValue
    mcv_value: typing.Annotated[int | None, pydantic.Field(alias="MCVValue")] = None
    way_point_type: WayPointType
    way_point_floor_id: int
    way_point_group_id: int
    way_point_entity_id: int
    way_point_show_range_min: int | None = None
    map_waypoint_range: int | None = None


class SubMission(BaseModel):
    id: int
    main_mission_id: int
    mission_active_plane_type: MissionActivePlaneType | None = None
    specified_plane_type_bits: int | None = None
    mission_json_path: str | None = None
    sort_id: int | None = None
    level_plane_id: int | None = None
    level_floor_id: int | None = None
    audio_emotion_state: str | None = None
    is_can_delete: bool = False
    logic_type: typing.Literal["Optional"] | None = None
    sound_effect_state: str | None = None
    take_type: TakeType | None = None
    take_param_int_list: list[int] | None = None
    maze_plane_id: int | None = None
    maze_floor_id: int | None = None
    maze_dimension_id: int | None = None
    finish_type: str | None = None
    param_type: ParamType | None = None
    param_int_1: int | None = None
    param_int_2: int | None = None
    param_int_3: int | None = None
    param_str_1: str | None = None
    param_int_list: list[int] | None = None
    param_item_list: list[item.Pair | Empty] | None = None
    finish_action_list: list[FinishAction] | None = None
    progress: int
    is_back_track: bool = False
    check_type: typing.Literal["SubmissionNotFinish"] | None = None
    check_param_int_1: int | None = None
    custom_value_list: list[int] | None = None
    process_group: int | None = None
    check_floor: bool = False
    sub_reward_id: int | None = None
    custom_value_reward: list[CustomValueReward] | None = None
    group_id_list: list[int] | None = None
    required_n_p_c_series_id_list: list[int] | None = None
    is_show: bool = True
    mute_nav: bool = False
    progress_group: int | None = None
    is_show_progress: bool = False
    mission_progress_type: typing.Literal["ShowProgress"] | None = None
    is_show_finish_effect: int | None = None
    is_show_start_hint: typing.Literal["New", "Update"] | None = None
    way_point_type: WayPointType | None = None
    is_track_by_message: bool = False
    message_group_id: int | None = None
    is_goto_ui_page: bool = False
    goto_id: int | None = None
    goto_param: list[int] | None = None
    way_point_floor_id: int | None = None
    way_point_group_id: int | None = None
    way_point_entity_id: int | None = None
    way_point_show_range_min: int | None = None
    map_waypoint_range: int | None = None
    froce_map_hint: bool = False
    story_line_id_list: list[int] | None = None
    story_line_id: int | None = None
    ignore_verse_param_list: list[str] | None = None
    multi_phase_waypoint: list[MultiPhaseWaypoint] | None = None
    optional_track_mode: typing.Literal["Always"] | None = None
    override_hint_max_distance: int | None = None


class DistanceCondition(BaseModel):
    use_override_range_min: bool = False
    override_range_min: int


class FloorCustomFloatConfig(BaseModel):
    typ: typing.Annotated[typing.Literal["RPG.GameCore.FloorCustomFloatConfig"], pydantic.Field(alias="$type")]
    default_value: typing.Literal[1] | None = None
    id: int
    name: str


class AssistWayPointFCVCondition(Model):
    target_fcv: typing.Annotated[FloorCustomFloatConfig, pydantic.Field(alias="TargetFCV")]
    validate_in_backtrace: bool = True
    operator: typing.Literal["Or"] | None = None


class AssistWayPointPropStateCondition(Model):
    target_prop_state: typing.Literal["Hidden", "Open"] | None = None
    use_logic_prop: bool = False
    logic_way_point_group_id: int | None = None
    logic_way_point_entity_id: int | None = None
    operator: typing.Literal["Or"] | None = None


class AssistWayPointRegionEraFlipStateCondition(Model):
    target_region_era_flip_state: typing.Literal["State02"] | None = None
    operator: typing.Literal["Or"] | None = None


class AssistWayPointTimelineStateCondition(Model):
    class TargetTimelineState(enum.Enum):
        L0_Grow = "L0_Grow"
        L0_Idle = "L0_Idle"
        L0_Root = "L0_Root"
        L1_Angle01 = "L1_Angle01"
        L1_Angle02 = "L1_Angle02"
        L1_Angle04 = "L1_Angle04"
        L1_GrownUp = "L1_GrownUp"
        L2_LiftUp = "L2_LiftUp"

    target_timeline_state: TargetTimelineState
    operator: typing.Literal["Or"] | None = None


AssistWayCondition = typing.Annotated[
    typing.Annotated[AssistWayPointFCVCondition, pydantic.Tag("AssistWayPointFCVCondition")]
    | typing.Annotated[AssistWayPointPropStateCondition, pydantic.Tag("AssistWayPointPropStateCondition")]
    | typing.Annotated[
        AssistWayPointRegionEraFlipStateCondition, pydantic.Tag("AssistWayPointRegionEraFlipStateCondition")
    ]
    | typing.Annotated[AssistWayPointTimelineStateCondition, pydantic.Tag("AssistWayPointTimelineStateCondition")],
    pydantic.Discriminator(get_discriminator),
]


class FinishConditionMain(BaseModel):
    class ConditionPack(BaseModel):
        condition_list: list[AssistWayCondition]
        operator: typing.Literal["Or"] | None = None

    condition_pack_list: list[ConditionPack]


class AssistWayPoint(BaseModel):
    way_point_type: WayPointType
    way_point_group_id: int
    way_point_entity_id: int
    submission_id: int | None = None
    use_prop_state: bool = False
    use_prop_state_backtrace: bool = False
    skip_when_sub_mission_finish: bool = False
    target_prop_state: typing.Literal["Open"] | None = None
    use_distance: bool = True
    use_logic_prop: bool = False
    use_override_range_min: bool = False
    distance_condition: DistanceCondition | Empty | None = None
    logci_way_point_group_id: int | None = None
    override_range_min: int | None = None
    can_backtrace: bool = False
    finish_condition_main: FinishConditionMain | Empty | None = None
    logci_way_point_entity_id: int | None = None


class AssistWayPointPack(BaseModel):
    assist_way_point_floor_id: int | None = None
    assist_way_point_region_id: int | None = None
    assist_way_point_list: list[AssistWayPoint]


class MissionInfo(BaseModel):
    main_mission_id: int
    prologue_sub_mssion_id: int | None = None
    start_sub_mission_list: list[int]
    finish_sub_mission_list: list[int]
    sub_mission_list: list[SubMission]
    mission_custom_value_list: list[MissionCustomValue] | None = None
    use_assist_way_point: bool = False
    custom_value_save_index_list: list[int] | None = None
    is_show: bool = True
    is_legacy_assist_way_point: bool = False
    assist_way_point_pack_list: list[AssistWayPointPack] | None = None
