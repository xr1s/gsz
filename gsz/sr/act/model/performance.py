import enum
import typing

import pydantic

from ...excel import Value, performance
from .base import Axis, BaseModel, Custom, FixedValue
from .camera import WaitFinishMode
from .target import Target


class AdvGroupEntity(BaseModel):
    is_override_art_model_offset: bool = False
    override_art_model_offset: Axis | None = None
    instance_id_list: list[int] | None = None
    task_enabled: bool = True


class AdvNpcFaceToPlayer(BaseModel):
    from_dialog: bool = True
    group_id: int | None = None
    group_npc_id: int | None = None
    player_in_group_id: int | None = None
    player_in_group_npc_id: int | None = None
    try_face_to_face: bool = True
    only_player_face_to_npc: bool = False
    npc_look_at_player: bool = True
    player_look_at_npc: bool = True
    stop_look_at_on_graph_end: bool = True
    turn_back_on_graph_end: bool = True
    steer_immediately: bool = False
    finish_immadiate: bool = False
    force_to_stand_by: bool | None = None
    wait_finish_mode: WaitFinishMode | None = None
    TaskEnabled: bool = True


class Type(enum.Enum):
    A = "A"
    C = "C"
    D = "D"
    E = "E"
    PlayVideo = "PlayVideo"


class MaskConfig(BaseModel):
    use_excel_data: typing.Literal[True]
    start_black: performance.BlackType
    end_black: performance.BlackType
    mask_color: typing.Literal["None"]


class CaptureNpc(BaseModel):
    """PerformanceTransition 的 CaptureNpcList"""

    group_id: FixedValue[int] | None = None
    group_npc_id: FixedValue[int] | None = None
    character_unique_name: Value[str] | None = None
    task_enabled: bool = True


class CaptureNPC(BaseModel):
    """LevelPerformanceInitialize 的 CaptureNPCList"""

    character_unique_name: str | None
    disable_emo_graph: bool = False
    group_id: int | None
    npc_id: int


class FindType(enum.Enum):
    ByOther = "ByOther"


class CaptureTeam(BaseModel):
    unique_name: str
    character_id: int | None = None
    find_type: FindType | None = None


class CreateCharacter(BaseModel):
    character_unique_name: str
    avatar_id: str
    area_name: str | None = None
    npc_appearance_preset: typing.Annotated[str | None, pydantic.Field(alias="NPCAppearancePreset")] = None
    override_replace_material_key_list: list[str] | None = None
    prop_switch_material_index: int | None = None
    anchor_name: str | None = None
    disable_emo_graph: bool = False


class Create(BaseModel):
    unique_name: Value[str] | None = None
    group_id: FixedValue[int]
    group_instance_id: FixedValue[int] | None = None


class CreateNpc(BaseModel):
    group_id: FixedValue[int] | None = None
    group_npc_id: FixedValue[int] | None = None
    npc_unique_name: typing.Annotated[Value[str] | None, pydantic.Field(alias="NPCUniqueName")] = None
    create_list: list[Create] | None = None
    default_idle_state_name: Value[str] | None = None
    task_enabled: bool = True


class CreateProp(BaseModel):
    group_id: FixedValue[int] | None = None
    group_prop_id: FixedValue[int] | None = None
    create_list: list["GroupEntityInfo"] | None = None
    task_enabled: bool = True


class DestroyNpc(BaseModel):
    group_id: int | None = None
    group_npc_id: int | None = None
    hide: bool = False
    destroy_list: list["GroupEntityInfo"] | None = None
    task_enabled: bool = True


class DestroyProp(BaseModel):
    target_type: Target
    id: FixedValue[int] | None = None
    group_id: FixedValue[int] | None = None
    destroy_list: list["GroupEntityInfo"] | None = None
    task_enabled: bool = True


class EntityVisiable(BaseModel):
    group_id: int
    group_npc_id: typing.Annotated[int, pydantic.Field(alias="GroupNPCID")]


class GroupEntityInfo(BaseModel):
    typ: typing.Annotated[typing.Literal["RPG.GameCore.GroupEntityInfo"], pydantic.Field(alias="$type")]
    group_id: FixedValue[int] | None = None
    group_instance_id: FixedValue[int] | None = None


class PropVisiable(BaseModel):
    group_id: int
    prop_id: int


class SwitchCharacterAnchor(BaseModel):
    is_local_player: bool = False
    character_unique_name: str | None = None
    area_name: Value[str] | Custom | None = None
    anchor_name: Value[str] | Custom | None = None
    level_area_key: Value[int] | Custom | None = None
    clear_special_vision: bool = False
    reset_animation: bool = True
    reset_camera: bool = True
    reset_turn_in_place: bool = False
    task_enabled: bool = True
