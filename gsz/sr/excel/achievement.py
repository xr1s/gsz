import enum
import typing

import pydantic
import typing_extensions

from .base import ModelID, Text, Value


class Rarity(enum.Enum):
    High = "High"
    Mid = "Mid"
    Low = "Low"


class ShowType(enum.Enum):
    HiddenDesc = "HiddenDesc"
    ShowAfterFinish = "ShowAfterFinish"


class RecordType(enum.Enum):
    AvatarShield = "AvatarShield"
    ConsecutiveLoginDays = "ConsecutiveLoginDays"
    SingleCure = "SingleCure"
    SingleHitCausesDamage = "SingleHitCausesDamage"
    SingleSkillCausesDamage = "SingleSkillCausesDamage"
    TotalLoginDays = "TotalLoginDays"
    World3CollectionCnt = "World3CollectionCnt"


class AchievementData(ModelID):
    achievement_id: int
    series_id: int
    quest_id: int
    linear_quest_id: int
    achievement_title: Text
    achievement_desc: Text
    hide_achievement_desc: Text | None = None
    achievement_desc_ps: typing.Annotated[Text | None, pydantic.Field(alias="AchievementDescPS")] = None
    param_list: tuple[Value[float], ...]
    priority: int
    rarity: Rarity
    show_type: ShowType | None = None
    record_type: RecordType | None = None
    ps_trophy_id: typing.Annotated[str, pydantic.Field(alias="PSTrophyID")]
    record_text: Text | None = None
    achievement_title_ps: typing.Annotated[Text | None, pydantic.Field(alias="AchievementTitlePS")] = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.achievement_id


class AchievementLevel(ModelID):
    level: int
    count: int
    level_icon_path: str

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.level


class AchievementSeries(ModelID):
    series_id: int
    series_title: Text
    main_icon_path: str
    icon_path: str
    gold_icon_path: str
    silver_icon_path: str
    copper_icon_path: str
    priority: int

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.series_id
