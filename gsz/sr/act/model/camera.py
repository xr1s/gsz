import enum
import typing

from .base import Axis, BaseModel, Empty
from .target import Target


class ActiveVirtualCamera(BaseModel):
    area_name: str | None = None
    anchor_name: str | None = None
    is_active: bool | None = None
    task_enabled: bool = True


class AttachPoint(enum.Enum):
    _0 = "0"
    Body = "Body"
    CameraRoot = "CameraRoot"
    Dice = "Dice"
    FocusPoint = "FocusPoint"
    Head = "Head"
    HintPoint = "HintPoint"
    Origin = "Origin"
    Root = "Root"
    RootM = "Root_M"
    RootPoint = "RootPoint"
    RotateRoot = "RotateRoot"
    WolfBro_Face = "WolfBro_Face"


class BlendType(enum.Enum):
    Custom = "Custom"
    Cut = "Cut"
    EaseIn = "EaseIn"
    EaseOut = "EaseOut"
    EaseInOut = "EaseInOut"


class BlendConfig(BaseModel):
    export_to_json: bool = False
    blend_type: BlendType | None = None
    custom_curve_name: str | None = None
    use_default_blend_curve: bool = False
    blend_time: float | None = None


class OverrideTasks(BaseModel):
    override_v_cam_blend_config: bool = False
    v_cam_blend_config: BlendConfig


class WaitFinishMode(enum.Enum):
    Default = "Default"
    WaitAnimFinish = "WaitAnimFinish"
    WaitFaceAngle = "WaitFaceAngle"


class BaseChangeParam(BaseModel):
    export_to_json: bool
    reset: bool = False
    zoom_ratio: float
    center_pos: Axis | None = None
    time: int
    change_curve_path: str
    recovery_time: float | None = None
    recovery_curve_path: str


class LookAtOffsetChangeParam(BaseModel):
    export_to_json: typing.Literal[True]
    target_value: Axis
    time: int
    change_curve_path: str
    recovery_time: int
    recovery_curve_path: str
    use_player_to_look_at_target_forward: typing.Literal[True]


class Freelook3rdConfig(BaseModel):
    export_to_json: typing.Literal[True]
    look_at_offset_change_param: LookAtOffsetChangeParam | None = None
    base_change_param: BaseChangeParam


class ScreenRange(BaseModel):
    in_range: Empty | None = None
    out_range: Empty | None = None


class CameraFreelook3rdConfig(BaseModel):
    config_type: typing.Literal["CameraFreelook3rdConfig"]
    freelook_3rd_config: Freelook3rdConfig


class OverrideShakeConfigV2(BaseModel):
    shake_scale: float | None = None
    shake_time: float | None = None
    shake_dir: Axis | None = None
    range_attenuation_delay: int | None = None
    range_attenuation_target: float | None = None
    range_attenuation_duration: int | None = None


class CameraShakeConfig(BaseModel):
    config_type: typing.Literal["ShakeTemplateName"]
    shake_templapte_name: str
    override_shake_config_v2: OverrideShakeConfigV2


class ShakeConfigV2(BaseModel):
    export_to_json: bool


class CameraState(enum.Enum):
    CastAnimation = "CastAnimation"
    CasterToTargetPerform = "CasterToTargetPerform"
    UseSkillPerform = "UseSkillPerform"


class NormalConfig(BaseModel):
    camera_state: CameraState
    template_name: str | None = None
    anchor_target_type: Target
    is_local_offset: bool = False
    anchor_offset: Axis
    anchor_ratio: float | None = None
    aim_target_type: Target
    aim_offset: Axis | None = None
    aim_ratio: float | None = None
    follow_pole_angle: int | None = None
    follow_elevation_angle: float | None = None
    follow_radius: float | None = None
    forbid_change_offset: bool = False
    follow_damp: float | None = None
    aim_damp: float | None = None
    reset_to_default: bool = True


class CloseupShotConfig(BaseModel):
    exit: bool = False
    trans_type_follow: Target | None = None
    follow_offset: Axis | None = None
    trans_type_aim: Target | None = None
    aim_offset: Axis | None = None
    override: bool = False


class ShowEntityConfig(BaseModel):
    export_to_json: bool = False
    show_target_type: Target
    is_target_ignore_camera_dither: bool = False
    is_alive_only: bool = True


class CameraConfig(BaseModel):
    normal_config: NormalConfig | None = None
    shake_template_name: str | None = None
    additive_normal_config: NormalConfig | None = None
    closeup_shot_config: CloseupShotConfig | None = None
    override_shake_config_v2: OverrideShakeConfigV2 | None = None
    shake_config_v2: ShakeConfigV2 | None = None
    blend_config: BlendConfig | None = None
    show_entity_config: ShowEntityConfig | None = None
    noise_config: Empty | None = None
