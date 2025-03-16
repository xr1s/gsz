import pathlib
import typing

import pydantic

from . import performance, predicate, talk
from ..excel import Value
from .base import Model as BaseModel, get_discriminator


class Model(BaseModel):
    typ: typing.Annotated[str, pydantic.Field(alias="$type")]


class BattlePerformInit(Model):
    area_prefab_path: str
    capture_team_light_list: list[performance.CaptureTeam]
    capture_team_dark_list: list[performance.CaptureTeam]


class BattlePerformTimeline(Model):
    timeline_path: pathlib.Path


class BattlePlayVideo(Model):
    video_id: int
    can_skip: bool = False


class CollectDataConditions(Model):
    task_id_list: list[int]
    main_mission_id_list: list[int]
    performance_id_list: list[int]
    performance_idds_list: typing.Annotated[list[int], pydantic.Field(alias="PerformanceIDDsList")]
    custom_value_main_mission_id_list: list[int]


class EndPerformance(Model):
    pass


class FinishLevelGraph(Model):
    make_owner_entity_die: bool = False


class LevelPerformanceInitialize(Model):
    performance_type: performance.Type
    area_prefab_path: str
    create_character_list: list[performance.CreateCharacter]
    capture_npc_list: list[performance.CaptureNPC]
    hide_npc: bool = False
    entity_visiable_list: list[performance.EntityVisiable] | None = None
    hide_prop: bool = False
    prop_visiable_list: list[performance.EntityVisiable] | None = None
    hide_local_player: bool = False
    first_camera_anchor: str | None = None
    streaming_sources_in_black_mask: list[str] | None = None
    streaming_sources_after_black_mask: list[str] | None = None
    mark_streaming_items: list[None] | None = None
    use_new_streaming_source_type: bool = False


class PlayAndWaitRogueSimpleTalk(Model):
    simple_talk_list: list[talk.RogueSimpleTalk]


class PlayOptionTalk(Model):
    option_list: list[talk.OptionTalkInfo]
    hide_selected: bool = False


class PlayRogueOptionTalk(Model):
    option_list: list[talk.RogueOptionTalk]


class PlayTimeline(Model):
    timeline_name: str
    type: typing.Literal["CutScene", "Discussion", "Story"] | None


class PredicateTaskList(Model):
    predicate: predicate.Predicate
    success_task_list: list[int]


class SetAsRogueDialogue(Model):
    pass


class SetBattleBGMState(Model):
    state_name: Value[str]


class SetMissionCustomValue(Model):
    submission_id: int
    mission_custom_value: predicate.MissionCustomValue
    custom_value: int


class ShowRogueTalkBg(Model):
    talk_bg_id: int


class ShowRogueTalkUI(Model):
    show: bool


class TriggerCustomString(Model):
    custom_string: Value[str]


class WaitCustomString(Model):
    custom_string: Value[str]
    go_next_immediately: bool = False
    reset_when_task_begin: bool = False
    wait_owner_only: bool = False


class WaitPerformanceEnd(Model):
    pass


Task = typing.Annotated[
    typing.Annotated[BattlePerformInit, pydantic.Tag("BattlePerformInit")]
    | typing.Annotated[BattlePerformTimeline, pydantic.Tag("BattlePerformTimeline")]
    | typing.Annotated[BattlePlayVideo, pydantic.Tag("BattlePlayVideo")]
    | typing.Annotated[CollectDataConditions, pydantic.Tag("CollectDataConditions")]
    | typing.Annotated[EndPerformance, pydantic.Tag("EndPerformance")]
    | typing.Annotated[FinishLevelGraph, pydantic.Tag("FinishLevelGraph")]
    | typing.Annotated[LevelPerformanceInitialize, pydantic.Tag("LevelPerformanceInitialize")]
    | typing.Annotated[PlayAndWaitRogueSimpleTalk, pydantic.Tag("PlayAndWaitRogueSimpleTalk")]
    | typing.Annotated[PlayOptionTalk, pydantic.Tag("PlayOptionTalk")]
    | typing.Annotated[PlayRogueOptionTalk, pydantic.Tag("PlayRogueOptionTalk")]
    | typing.Annotated[PlayTimeline, pydantic.Tag("PlayTimeline")]
    | typing.Annotated[PredicateTaskList, pydantic.Tag("PredicateTaskList")]
    | typing.Annotated[SetAsRogueDialogue, pydantic.Tag("SetAsRogueDialogue")]
    | typing.Annotated[SetBattleBGMState, pydantic.Tag("SetBattleBGMState")]
    | typing.Annotated[SetMissionCustomValue, pydantic.Tag("SetMissionCustomValue")]
    | typing.Annotated[ShowRogueTalkBg, pydantic.Tag("ShowRogueTalkBg")]
    | typing.Annotated[ShowRogueTalkUI, pydantic.Tag("ShowRogueTalkUI")]
    | typing.Annotated[TriggerCustomString, pydantic.Tag("TriggerCustomString")]
    | typing.Annotated[WaitCustomString, pydantic.Tag("WaitCustomString")]
    | typing.Annotated[WaitPerformanceEnd, pydantic.Tag("WaitPerformanceEnd")],
    pydantic.Discriminator(get_discriminator),
]
