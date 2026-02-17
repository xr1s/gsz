from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from ..excel import achievement


class AchievementData(View[excel.AchievementData]):
    ExcelOutput: typing.Final = excel.AchievementData

    @property
    def id(self) -> int:
        return self._excel.achievement_id

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.achievement_title)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.achievement_desc)

    @functools.cached_property
    def params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)

    @functools.cached_property
    def hide_desc(self) -> str | None:
        return self._game.text(self._excel.hide_achievement_desc) if self._excel.hide_achievement_desc else None

    @property
    def series_id(self) -> int:
        return self._excel.series_id

    @functools.cached_property
    def __series(self) -> AchievementSeries:
        series = self._game.achievement_series(self._excel.series_id)
        assert series is not None
        return series

    def series(self) -> AchievementSeries:
        return self.__series

    @property
    def show_type(self) -> achievement.ShowType | None:
        return self._excel.show_type

    @property
    def priority(self) -> int:
        return self._excel.priority

    @property
    def rarity(self) -> achievement.Rarity:
        return self._excel.rarity


class AchievementLevel(View[excel.AchievementLevel]):
    ExcelOutput: typing.Final = excel.AchievementLevel


class AchievementSeries(View[excel.AchievementSeries]):
    ExcelOutput: typing.Final = excel.AchievementSeries

    @property
    def id(self) -> int:
        return self._excel.series_id

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.series_title)
