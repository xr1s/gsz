import enum
import typing

import pydantic

from ...excel import Text
from . import predicate
from .base import BaseModel


class Background(BaseModel):
    image_path: str | None = None
    cg_id: int | None = None


class DialogueEvent(BaseModel):
    dialogue_event_id: int | None = None
    failure_custom_string: str | None = None
    success_custom_string: str | None = None


class RogueSimpleTalk(BaseModel):
    talk_sentence_id: int
    text_speed: int | None = None
    talk_bg_id: int | None = None


class TargetBehavior(BaseModel):
    unique_name: str | None = None
    use_mouth_talk: bool = False


class SimpleTalk(BaseModel):
    talk_sentence_id: int | None = None
    text_speed: float | None = None
    protect_time: float | None = None
    force_to_next_time: int | None = None


class OptionIconType(enum.Enum):
    AbyssIcon = "AbyssIcon"
    ActivityIcon = "ActivityIcon"
    ChallengeBossIcon = "ChallengeBossIcon"
    ChallengeStoryIcon = "ChallengeStoryIcon"
    ChatBackIcon = "ChatBackIcon"
    ChatContinueIcon = "ChatContinueIcon"
    ChatIcon = "ChatIcon"
    ChatLoopIcon = "ChatLoopIcon"
    ChatMissionIcon = "ChatMissionIcon"
    ChatOutIcon = "ChatOutIcon"
    CheckIcon = "CheckIcon"
    GeneralActivityIcon = "GeneralActivityIcon"
    HeartDialTracer = "HeartDialTracer"
    OrigamiBirdIcon = "OrigamiBirdIcon"
    PickUpIcon = "PickUpIcon"
    RogueHeita = "RogueHeita"
    SecretMissionIcon = "SecretMissionIcon"
    ShopIcon = "ShopIcon"
    SpecialChatIcon = "SpecialChatIcon"
    SwitchHandIcon = "SwitchHandIcon"

    def wiki(self) -> str:  # noqa: PLR0911, PLR0912
        match self:
            case OptionIconType.AbyssIcon:
                return "Abyss <!-- 未上传 -->"
            case OptionIconType.ActivityIcon | OptionIconType.GeneralActivityIcon:
                return "活动"
            case OptionIconType.ChallengeBossIcon:
                return "ChallengeBoss <!-- 未上传 -->"
            case OptionIconType.ChallengeStoryIcon:
                return "ChallengeStory <!-- 未上传 -->"
            case OptionIconType.ChatBackIcon:
                return "返回"
            case OptionIconType.ChatContinueIcon:
                return "继续"
            case OptionIconType.ChatLoopIcon | OptionIconType.ChatIcon:
                return "对话"
            case OptionIconType.ChatMissionIcon:
                return "任务"
            case OptionIconType.ChatOutIcon:
                return "退出"
            case OptionIconType.CheckIcon:
                return "调查"
            case OptionIconType.HeartDialTracer:
                return "ClockBoyTalkMood <!-- 未上传 -->"
            case OptionIconType.OrigamiBirdIcon:
                return "折纸小鸟"
            case OptionIconType.PickUpIcon:
                return "拾取"
            case OptionIconType.RogueHeita:
                return "黑塔"
            case OptionIconType.SecretMissionIcon:
                return "事件"
            case OptionIconType.ShopIcon:
                return "商店"
            case OptionIconType.SpecialChatIcon:
                return "SpecialChatIcon <!-- 未上传，金色的 ChatIcon -->"
            case OptionIconType.SwitchHandIcon:
                return "SwitchHandIcon <!-- 未上传，大手 -->"


class RogueOptionTalk(BaseModel):
    rogue_option_id: int | None = None
    talk_sentence_id: int | None = None
    option_textmap_id: Text | None = None
    option_icon_type: OptionIconType | None = None
    trigger_custom_string: str | None = None
    delete_after_selection: bool = False
    has_triggered: bool = False


class OptionTalkInfo(BaseModel):
    typ: typing.Annotated[typing.Literal["RPG.GameCore.OptionTalkInfo"], pydantic.Field(alias="$type")]
    talk_sentence_id: int | None = None
    option_textmap_id: Text | None = None
    option_icon_type: OptionIconType | None = None
    trigger_custom_string: str | None = None
    delete_after_selection: bool = False
    finish_key: typing.Literal["0"] | None = None
    has_triggered: bool = False
    submission_id: int | None = None
    talk_event_id: int | None = None
    """一般是选择某个选项会有道具奖励"""
    visible_filter: predicate.Predicate | None = None


class OptionTalk(typing.Protocol):
    talk_sentence_id: int | None
    option_textmap_id: Text | None
    option_icon_type: OptionIconType | None
    trigger_custom_string: str | None
