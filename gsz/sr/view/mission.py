import functools
import typing

from .. import excel
from ..excel import mission
from .base import View


class MainMission(View[excel.MainMission]):
    ExcelOutput: typing.Final = excel.MainMission

    @functools.cached_property
    def name(self) -> str:
        return "" if self._excel.name is None else self._game.text(self._excel.name)

    @property
    def type(self) -> mission.MainType:
        return self._excel.type


class SubMission(View[excel.SubMission]):
    ExcelOutput: typing.Final = excel.SubMission

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.descrption_text)

    @functools.cached_property
    def target(self) -> str:
        return self._game.text(self._excel.target_text)
