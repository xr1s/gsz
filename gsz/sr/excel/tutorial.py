import enum
import typing

import typing_extensions

from .base import Model, ModelID, Text


class TutorialGuideData(ModelID):
    id_: int
    image_path: str
    desc_text: Text | None = None
    platform_type: typing.Literal["Mobile", "PS"] | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_


class Type(enum.Enum):
    Battle = 1
    Adventure = 2
    System = 3
    SimulatedUniverse = 4

    @typing_extensions.override
    def __str__(self) -> str:
        match self:
            case self.Battle:
                return "战斗"
            case self.Adventure:
                return "冒险"
            case self.System:
                return "系统"
            case self.SimulatedUniverse:
                return "模拟宇宙"


class ShowType(enum.Enum):
    AutoShow = "AutoShow"
    AutoShowInMaze = "AutoShowInMaze"
    BattleStart = "BattleStart"
    Hide = "Hide"
    NonTutorial = "NonTutorial"


class TriggerType(enum.Enum):
    CarryMazeBuff = "CarryMazeBuff"
    DestructProp = "DestructProp"
    EnterBattle = "EnterBattle"
    EnterBattleByChallengeType = "EnterBattleByChallengeType"
    EnterBattleByStageType = "EnterBattleByStageType"
    FinishMainMission = "FinishMainMission"
    FinishQuest = "FinishQuest"
    FinishSubMission = "FinishSubMission"
    GameMode = "GameMode"
    GetAvatar = "GetAvatar"
    GetNewItemByType = "GetNewItemByType"
    OpenChest = "OpenChest"
    PlayerLevel = "PlayerLevel"
    ShowUIDialog = "ShowUIDialog"
    ShowUIPage = "ShowUIPage"
    TakeSubMission = "TakeSubMission"
    TaskUnlock = "TaskUnlock"
    TriggerPuzzle = "TriggerPuzzle"
    TutorialFinish = "TutorialFinish"


class TriggerParam(Model):
    trigger_type: TriggerType
    trigger_param: str


class TutorialGuideGroup(ModelID):
    group_id: int
    tutorial_guide_id_list: list[int]
    tutorial_type: Type
    can_review: bool = False
    tutorial_show_type: ShowType | None = None
    order: int | None = None
    trigger_params: list[TriggerParam]
    finish_trigger_params: list[TriggerParam]
    message_text: Text | None = None
    reward_id: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.group_id
