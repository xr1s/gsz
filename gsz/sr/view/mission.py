from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from ..act.model import mission as actmission
    from ..excel import mission


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
    def __info(self) -> actmission.MissionInfo:
        from ..act.model.mission import MissionInfo

        path = MainMission.__MISSION_INFO_PATH.format(main_mission_id=self._excel.main_mission_id)
        return MissionInfo.model_validate_json(self._game.base.joinpath(path).read_bytes())

    @functools.cached_property
    def __sub_missions(self) -> list[SubMission]:
        return list(self._game.sub_mission(sub.id for sub in self.__info.sub_mission_list))

    def sub_missions(self) -> collections.abc.Iterable[SubMission]:
        return (SubMission(self._game, sub._excel) for sub in self.__sub_missions)


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
