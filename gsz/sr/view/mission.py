from __future__ import annotations

import functools
import typing

import pydantic

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .. import act
    from ..excel import mission
    from .performance import Performance


class ChronicleConclusion(View[excel.ChronicleConclusion]):
    ExcelOutput: typing.Final = excel.ChronicleConclusion

    @functools.cached_property
    def __mission(self) -> MainMission:
        mission = self._game.main_mission(self._excel.mission_id)
        assert mission is not None
        return mission

    def mission(self) -> MainMission:
        return MainMission(self._game, self.__mission._excel)

    @functools.cached_property
    def conclusion(self) -> str:
        return self._game.text(self._excel.mission_conclusion)


class MainMission(View[excel.MainMission]):
    ExcelOutput: typing.Final = excel.MainMission

    @functools.cached_property
    def name(self) -> str:
        return "" if self._excel.name is None else self._game.text(self._excel.name)

    @property
    def type(self) -> mission.MainType:
        return self._excel.type

    __MISSION_INFO_PATH = "Config/Level/Mission/{main_mission_id}/MissionInfo_{main_mission_id}.json"

    @functools.cached_property
    def __sub_missions(self) -> list[SubMission]:
        # 只为了取 SubMission，避免引入 act，因为引入 act 非常耗时，Task 太复杂了
        class ActSubMission(pydantic.BaseModel):
            id: typing.Annotated[int, pydantic.Field(alias="ID")]

        class ActMissionInfo(pydantic.BaseModel):
            sub_mission_list: typing.Annotated[list[ActSubMission], pydantic.Field(alias="SubMissionList")]

        path = MainMission.__MISSION_INFO_PATH.format(main_mission_id=self._excel.main_mission_id)
        path = self._game.base.joinpath(path)
        if not path.exists():
            return []
        act_main_mission = ActMissionInfo.model_validate_json(path.read_bytes())
        return list(filter(None, (self._game.sub_mission(sub.id) for sub in act_main_mission.sub_mission_list)))

    def sub_missions(self) -> collections.abc.Iterable[SubMission]:
        return (SubMission(self._game, sub._excel) for sub in self.__sub_missions)

    @functools.cached_property
    def __info(self) -> act.model.MissionInfo:
        from .. import act

        path = MainMission.__MISSION_INFO_PATH.format(main_mission_id=self._excel.main_mission_id)
        return act.model.MissionInfo.model_validate_json(self._game.base.joinpath(path).read_bytes())

    def info(self) -> act.MissionInfo:
        from .. import act

        return act.MissionInfo(self._game, self.__info)


class SubMission(View[excel.SubMission]):
    ExcelOutput: typing.Final = excel.SubMission

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def description(self) -> str | None:
        return None if self._excel.descrption_text is None else self._game.text(self._excel.descrption_text)

    @functools.cached_property
    def target(self) -> str | None:
        return None if self._excel.target_text is None else self._game.text(self._excel.target_text)

    @functools.cached_property
    def __performance(self) -> Performance | None:
        return self._game.performance_e(self._excel.sub_mission_id)

    def performance(self) -> Performance | None:
        from .performance import Performance

        return None if self.__performance is None else Performance(self._game, self.__performance._excel)
