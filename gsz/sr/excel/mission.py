import enum
import typing

import typing_extensions

from .base import Model, ModelID, Text


class MissionChapterConfig(ModelID):
    id_: int
    chapter_name: Text
    stage_name: str | None = None  # 仅在 1.1 及之后出现
    chapter_desc: str
    chapter_type: typing.Literal["Activity"] | None = None
    link_chapter_list: list[int] | None = None  # 仅在 1.5 及之后出现
    chapter_display_priority: int
    origin_main_mission: int | None = None
    final_main_mission: int | None = None
    chapter_icon_path: str
    chapter_figure_icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class MainType(enum.Enum):
    Branch = "Branch"
    """冒险任务"""
    Companion = "Companion"
    """同行任务"""
    Daily = "Daily"
    """日常任务"""
    Gap = "Gap"
    """间章任务"""
    Main = "Main"
    """主线任务"""

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case self.Branch:
                return "冒险任务"
            case self.Companion:
                return "同行任务"
            case self.Daily:
                return "日常任务"
            case self.Gap:
                return "间章任务"
            case self.Main:
                return "主线任务"


class Operation(enum.Enum):
    And = "And"
    Or = "Or"


class ParamType(enum.Enum):
    Auto = "Auto"
    HeliobusPhaseReach = "HeliobusPhaseReach"
    Manual = "Manual"
    MultiSequence = "MultiSequence"
    MuseumPhaseRenewPointReach = "MuseumPhaseRenewPointReach"
    PlayerLevel = "PlayerLevel"
    Sequence = "Sequence"
    SequenceNextDay = "SequenceNextDay"
    WorldLevel = "WorldLevel"


class Param(Model):
    type: ParamType
    value: int | None = None


class EmotionState(enum.Enum):
    No = ""
    BgmD1 = "State_BGM_D7"
    BgmE1 = "State_Bgm_E1"
    BgmE2 = "State_Bgm_E2"
    BgmE3 = "State_Bgm_E3"
    BgmE4 = "State_Bgm_E4"
    BgmE5 = "State_Bgm_E5"
    BgmE6 = "State_Bgm_E6"
    BgmE7 = "State_Bgm_E7"
    BgmE8 = "State_Bgm_E8"
    BgmE9 = "State_Bgm_E9"
    BgmED = "State_Bgm_E_D"
    BgmEnding = "State_Bgm_Ending"
    Esilence = "State_Esilence"
    Hollowing = "State_Hollowing"
    HollowingD = "State_Hollowing_D"
    Investigate = "State_Investigate"
    Joyful = "State_Joyful"
    Mysterious = "State_Mysterious"
    Nervous = "State_Nervous"
    Relaxing = "State_Relaxing"
    ServantMini = "State_ServantMini"
    Severe = "State_Severe"
    Sorrow = "State_Sorrow"
    Suspense = "State_Suspense"
    Tense = "State_Tense"
    Warm = "State_Warm"


class SubType(enum.Enum):
    Activity = "Activity"
    Game = "Game"
    Rogue = "Rogue"
    System = "System"
    World = "World"


class MainMission(ModelID):
    main_mission_id: int
    type: MainType
    sub_type: SubType | None = None  # 仅在 3.0 及之后出现
    world_id: int | None = None  # 仅在 3.0 及之后出现
    display_priority: int
    is_display_activity_icon: bool = False
    is_in_raid: bool = False
    next_main_mission_list: list[None]  #  只有空 []
    name: Text | None = None
    take_type_a: ParamType | None = None  # 仅在 1.0 出现
    take_param_a_int_1: int | None = None  # 仅在 1.0 出现
    take_param_a_int_list: list[int] | None = None  # 仅在 1.0 出现
    take_type_b: ParamType | None = None  # 仅在 1.0 出现
    take_param_b_int_1: int | None = None  # 仅在 1.0 出现
    take_param_b_int_list: list[int] | None = None  # 仅在 1.0 出现
    take_operation: Operation | None = None
    begin_operation: Operation | None = None
    take_param: list[Param] | None = None
    begin_param: list[Param]
    next_track_main_mission: int | None = None
    is_show_red_dot: bool = False  # 仅在 1.2 及之前出现
    track_weight: int | None = None
    mission_suspend: typing.Literal[1] | None = None  #  仅在 1.6 及之前出现，只有 1
    mission_advance: typing.Literal[1] | None = None
    reward_id: int | None = None
    display_reward_id: int | None = None
    audio_emotion_state: EmotionState | None = None  # 仅在 1.4 及之前出现
    mission_pack: int | None = None
    chapter_id: int | None = None
    sub_reward_list: list[int]
    story_line_id_list: list[None] | None = None  # 仅在 2.0 出现

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.main_mission_id


class MapNPC(Model):
    HEJINHDPIED: int
    DHBLMALKKHI: int


class MapProp(Model):
    HEJINHDPIED: int
    FDAKPBACCBE: int


class FinishActorType(enum.Enum):
    AddMissionItem = "addMissionItem"
    AddRecoverMissionItem = "addRecoverMissionItem"
    ChangeLineup = "ChangeLineup"
    DelMission = "delMission"
    DelMissionItem = "delMissionItem"
    Recover = "Recover"


class WayPointType(enum.Enum):
    Anchor = "Anchor"
    Monster = "Monster"
    NPC = "NPC"
    Prop = "Prop"


# 1.1 及之后一堆废弃字段，绷不住了
class SubMissionV10(Model):
    next_sub_mission_id: int | None = None
    next_sub_mission_list: list[int] | None = None
    main_mission_id: int | None = None
    maze_plane_id: int | None = None
    maze_floor_id: int | None = None
    map_npc_list: list[MapNPC] | None = None
    map_prop_list: list[MapProp] | None = None
    exclusive_group_list: list[None] | None = None
    is_show: bool = False
    mute_nav: bool = False
    progress_group: int | None = None
    is_show_progress: bool = False
    is_show_finish_effect: typing.Literal[1, 2] | None = None
    is_show_start_hint: typing.Literal["New", "Update"] | None = None
    way_point_type: WayPointType | None = None
    way_point_floor_id: int | None = None
    way_point_group_id: int | None = None
    way_point_entity_id: int | None = None
    way_point_show_range_min: int | None = None
    map_waypoint_icon_type: int | None = None
    map_waypoint_range: int | None = None
    finish_actor_type: FinishActorType | None = None
    finish_actor_para: str | None = None
    froce_map_hint: bool = False
    audio_emotion_state: EmotionState | None = None
    process_group: int | None = None
    sort_id: int | None = None
    sub_custom_value_list: list[int] | None = None
    sub_reward_id: int | None = None
    custom_value_reward: list[int] | None = None


class SubMission(SubMissionV10, ModelID):
    sub_mission_id: int
    target_text: Text | None = None
    descrption_text: Text | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.sub_mission_id
