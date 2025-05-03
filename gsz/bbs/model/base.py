import enum
import typing

import pydantic


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


class GameId(enum.Enum):
    HonkaiImpact3 = 1
    """崩坏3"""
    GenshinImpact = 2
    """原神"""
    GunsGirlSchoolDayZ = 3
    """崩坏学院2"""
    TearsOfThemis = 4
    """未定事件簿"""
    Villa = 5
    """大别野"""
    HonkaiStarRail = 6
    """崩坏：星穹铁道"""
    ZenlessZoneZero = 8
    """绝区零"""


T = typing.TypeVar("T")


class Response(Model, typing.Generic[T]):
    retcode: int
    message: str
    data: T
