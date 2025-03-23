import enum
import typing

import pydantic

from ..excel import Text
from .base import Model


class DialogueEvent(Model):
    dialogue_event_id: int | None = None
    success_custom_string: str | None = None
    failure_custom_string: str | None = None


class RogueSimpleTalk(Model):
    talk_bg_id: int | None = None
    talk_sentence_id: int
    text_speed: int | None = None


class OptionIconType(enum.Enum):
    AbyssIcon = "AbyssIcon"
    ChallengeStoryIcon = "ChallengeStoryIcon"
    ChatBackIcon = "ChatBackIcon"
    ChatContinueIcon = "ChatContinueIcon"
    ChatIcon = "ChatIcon"
    ChatLoopIcon = "ChatLoopIcon"
    ChatMissionIcon = "ChatMissionIcon"
    ChatOutIcon = "ChatOutIcon"
    CheckIcon = "CheckIcon"
    GeneralActivityIcon = "GeneralActivityIcon"
    OrigamiBirdIcon = "OrigamiBirdIcon"
    PickUpIcon = "PickUpIcon"
    RogueHeita = "RogueHeita"
    SecretMissionIcon = "SecretMissionIcon"
    ShopIcon = "ShopIcon"
    SpecialChatIcon = "SpecialChatIcon"


class RogueOptionTalk(Model):
    talk_sentence_id: int | None = None
    option_textmap_id: Text | None = None
    option_icon_type: OptionIconType | None = None
    rogue_option_id: int | None = None
    trigger_custom_string: str | None = None
    has_triggered: bool = False
    delete_after_selection: bool = False


class OptionTalkInfo(Model):
    typ: typing.Annotated[typing.Literal["RPG.GameCore.OptionTalkInfo"], pydantic.Field(alias="$type")]
    talk_sentence_id: int
    option_icon_type: OptionIconType
    trigger_custom_string: str
