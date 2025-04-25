import enum
import typing

from .base import BaseModel


class ActionName(enum.Enum):
    Map = "Maze_Map"
    Cancel = "Menu_Cancel"
    ClosePage = "Menu_ClosePage"
    Confirm = "Menu_Confirm"
    MazeAttack = "Menu_MazeAttack"
    MazeSkill = "Menu_MazeSkill"
    PhoneOrQuitGame = "Menu_PhoneOrQuitGame"
    SwitchAvatar2 = "Menu_SwitchAvatar2"
    TalkClick1 = "Menu_TalkClick1"
    TalkClick2 = "Menu_TalkClick2"
    TalkClick3 = "Menu_TalkClick3"
    TinyGameEvent = "Menu_TinyGameEvent"
    UnchangeBack = "Menu_UnchangeBack"
    UnchangeLeftBumper = "Menu_UnchangeLeftBumper"
    UnchangeLeftStickDown = "Menu_UnchangeLeftStickDown"
    UnchangeLeftStickLeft = "Menu_UnchangeLeftStickLeft"
    UnchangeLeftStickRight = "Menu_UnchangeLeftStickRight"
    UnchangeLeftStickUp = "Menu_UnchangeLeftStickUp"
    UnchangeOption = "Menu_UnchangeOption"
    UnchangeRightBumper = "Menu_UnchangeRightBumper"
    UnchangeX = "Menu_UnchangeX"
    UnchangeY = "Menu_UnchangeY"


class Direction(enum.Enum):
    Down = "Down"
    Left = "Left"
    LeftDown = "LeftDown"
    LeftUp = "LeftUp"
    Right = "Right"
    RightDown = "RightDown"
    RightUp = "RightUp"
    Up = "Up"


class ShowConfig(BaseModel):
    use_custom_config: bool = False
    scale_x: float | None = None
    scale_y: float | None = None
    offset_x: float | None = None
    offset_y: float | None = None


class ContextConfig(BaseModel):
    type: typing.Literal["MainPage", "Normal"] | None = None
    name: str | None = None


class GuideHintType(enum.Enum):
    ClickCircle = "ClickCircle"
    ClickRect = "ClickRect"
    NormalCircle = "NormalCircle"
    NormalRect = "NormalRect"
    SwipeAToB = "SwipeAToB"
    SwipeLeft = "SwipeLeft"


class GuideTextType(enum.Enum):
    CommonCenterTalk = "CommonCenterTalk"
    InfoTip = "InfoTip"
    RogueCenterTalk = "RogueCenterTalk"
    RogueTalk = "RogueTalk"
    Talk = "Talk"
    TopCenterTip = "TopCenterTip"
