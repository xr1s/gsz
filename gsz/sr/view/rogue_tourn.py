from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from .misc import MazeBuff
    from ..excel import rogue_tourn


class RogueTournBuff(View[excel.RogueTournBuff]):
    ExcelOutput: typing.Final = excel.RogueTournBuff


class RogueTournBuffType(View[excel.RogueTournBuffType]):
    ExcelOutput: typing.Final = excel.RogueTournBuffType


class RogueTournFormula(View[excel.RogueTournFormula]):
    ExcelOutput: typing.Final = excel.RogueTournFormula

    @property
    def name(self) -> str:
        return self.maze_buff.name

    @property
    def desc(self) -> str:
        return self.maze_buff.desc

    @property
    def param_list(self) -> tuple[float, ...]:
        return self.maze_buff.param_list

    @property
    def tourn_mode(self) -> rogue_tourn.Mode | None:
        """None 应该是测试数据，观察到 None 里有一些重复的数据"""
        return self._excel.tourn_mode

    @property
    def display(self) -> RogueTournFormulaDisplay:
        display = self._game.rogue_tourn_formula_display(self._excel.formula_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def maze_buff(self) -> MazeBuff:
        maze_buff = self._game.rogue_maze_buff(self._excel.maze_buff_id)
        return next(iter(maze_buff))


class RogueTournFormulaDisplay(View[excel.RogueTournFormulaDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournFormulaDisplay


class RogueTournHandbookMiracle(View[excel.RogueTournHandbookMiracle]):
    ExcelOutput: typing.Final = excel.RogueTournHandbookMiracle


class RogueTournMiracle(View[excel.RogueTournMiracle]):
    ExcelOutput: typing.Final = excel.RogueTournMiracle


class RogueTournTitanBless(View[excel.RogueTournTitanBless]):
    ExcelOutput: typing.Final = excel.RogueTournTitanBless


class RogueTournWeeklyChallenge(View[excel.RogueTournWeeklyChallenge]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyChallenge


class RogueTournWeeklyDisplay(View[excel.RogueTournWeeklyDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyDisplay
