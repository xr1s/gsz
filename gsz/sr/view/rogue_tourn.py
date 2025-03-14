from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View
from .misc import MazeBuff

if typing.TYPE_CHECKING:
    from ..excel import rogue_tourn
    from .rogue import RogueMiracle, RogueMiracleDisplay, RogueMiracleEffectDisplay


class RogueTournBuff(View[excel.RogueTournBuff]):
    ExcelOutput: typing.Final = excel.RogueTournBuff

    @property
    def name(self) -> str:
        return self.__maze_buff.name

    @property
    def desc(self) -> str:
        return self.__maze_buff.desc

    @property
    def param_list(self) -> tuple[float, ...]:
        return self.__maze_buff.param_list

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        buff = self._game.maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert buff is not None
        return buff

    def buff(self) -> MazeBuff:
        return MazeBuff(self._game, self.__maze_buff._excel)


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

    @functools.cached_property
    def __rogue_tourn_formula_display(self) -> RogueTournFormulaDisplay:
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

    @property
    def name(self) -> str:
        if self.__rogue_miracle_display.name != "":
            return self.__rogue_miracle_display.name
        return ""

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.name)  # pyright: ignore[reportPrivateUsage]

    @property
    def desc(self) -> str:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc
        return self.__rogue_miracle_display.desc

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc_param_list
        return self.__rogue_miracle_display.desc_param_list

    @property
    def category(self) -> rogue_tourn.MiracleCategory:
        return self._excel.miracle_category

    @property
    def bg_desc(self) -> str:
        return self.__rogue_miracle_display.bg_desc

    @property
    def tag(self) -> str:
        return self.__rogue_miracle_display.tag

    @functools.cached_property
    def __rogue_miracle_display(self) -> RogueMiracleDisplay:
        display = self._game.rogue_miracle_display(self._excel.miracle_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def __rogue_miracle_effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self._excel.miracle_effect_display_id is None:
            return None
        display = self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        assert display is not None
        return display

    def display(self) -> RogueMiracleDisplay:
        from .rogue import RogueMiracleDisplay

        return RogueMiracleDisplay(self._game, self.__rogue_miracle_display._excel)

    def effect_display(self) -> RogueMiracleEffectDisplay | None:
        from .rogue import RogueMiracleEffectDisplay

        if self.__rogue_miracle_effect_display is None:
            return None
        return RogueMiracleEffectDisplay(self._game, self.__rogue_miracle_effect_display._excel)

    @functools.cached_property
    def __rogue_miracle(self) -> RogueMiracle | None:
        return self._game.rogue_miracle_name(self.name)

    def rogue_miracle(self) -> RogueMiracle | None:
        from .rogue import RogueMiracle

        if self.__rogue_miracle is not None:
            return RogueMiracle(self._game, self.__rogue_miracle._excel)
        return None

    def wiki(self) -> str:
        modes = ["差分宇宙"] if self.__rogue_miracle is None else ["模拟宇宙", "差分宇宙"]
        return self._game._template_environment.get_template("奇物.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            miracle=self.__rogue_miracle, tourn_miracle=self, modes=modes
        )


class RogueTournTitanBless(View[excel.RogueTournTitanBless]):
    ExcelOutput: typing.Final = excel.RogueTournTitanBless


class RogueTournWeeklyChallenge(View[excel.RogueTournWeeklyChallenge]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyChallenge


class RogueTournWeeklyDisplay(View[excel.RogueTournWeeklyDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyDisplay
