from __future__ import annotations
import functools
import itertools
import typing

from .. import excel
from ..excel import rogue
from .base import View
from .misc import MazeBuff

if typing.TYPE_CHECKING:
    import collections.abc
    from ..excel import rogue_tourn
    from .rogue import RogueMiracle, RogueMiracleDisplay, RogueMiracleEffectDisplay, RogueBuff


class RogueTournBuff(View[excel.RogueTournBuff]):
    ExcelOutput: typing.Final = excel.RogueTournBuff

    @property
    def name(self) -> str:
        return self.__maze_buff.name

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.__maze_buff.name.replace("\xa0", ""))  # pyright: ignore[reportPrivateUsage]

    @property
    def level(self) -> int:
        return self.__maze_buff.level

    @property
    def desc(self) -> str:
        return self.__maze_buff.desc

    @property
    def param_list(self) -> tuple[float, ...]:
        return self.__maze_buff.param_list

    @property
    def category(self) -> rogue.BuffCategory | None:
        return self._excel.rogue_buff_category

    @property
    def tag(self) -> int:
        return self._excel.rogue_buff_tag

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert buff is not None
        return buff

    def maze_buff(self) -> MazeBuff:
        return MazeBuff(self._game, self.__maze_buff._excel)

    @functools.cached_property
    def __rogue_buffs(self) -> list[RogueBuff]:
        return list(self._game.rogue_buff_name(self.name))

    def rogue_buffs(self) -> collections.abc.Iterable[RogueBuff]:
        from .rogue import RogueBuff

        return (RogueBuff(self._game, buff._excel) for buff in self.__rogue_buffs)

    @functools.cached_property
    def __rogue_tourn_buff_type(self) -> RogueTournBuffType:
        typ = self._game.rogue_tourn_buff_type(self._excel.rogue_buff_type)
        assert typ is not None
        return typ

    def type(self) -> RogueTournBuffType:
        from .rogue_tourn import RogueTournBuffType

        return RogueTournBuffType(self._game, self.__rogue_tourn_buff_type._excel)

    @functools.cached_property
    def __rogue_tourn_buff_group(self) -> list[RogueTournBuffGroup]:
        return self._game.rogue_tourn_buff_tag_groups(self.tag)

    def tag_group(self) -> collections.abc.Iterable[RogueTournBuffGroup]:
        return (RogueTournBuffGroup(self._game, group._excel) for group in self.__rogue_tourn_buff_group)

    @functools.cached_property
    def __tag_drops(self) -> list[RogueTournBuff]:
        return list(itertools.chain.from_iterable(group.drops() for group in self.__rogue_tourn_buff_group))

    def tag_drops(self) -> collections.abc.Iterable[RogueTournBuff]:
        return (RogueTournBuff(self._game, drop._excel) for drop in self.__tag_drops)

    @functools.cached_property
    def __rogue_tourn_buffs(self) -> list[RogueTournBuff]:
        return self._game.rogue_tourn_buff_name(self.name)

    def tourn_buffs(self) -> collections.abc.Iterable[RogueTournBuff]:
        return (RogueTournBuff(self._game, buff._excel) for buff in self.__rogue_tourn_buffs)

    @functools.cached_property
    def __degrade(self) -> RogueTournBuff:
        if self._excel.maze_buff_level == 1:
            return self
        buff = self._game.rogue_tourn_buff(self._excel.maze_buff_id, 1)
        assert buff is not None
        return buff

    @functools.cached_property
    def __upgrade(self) -> RogueTournBuff | None:
        if self.__maze_buff.level_max == 1:
            return None
        if self._excel.maze_buff_level == 2:
            return self
        return self._game.rogue_tourn_buff(self._excel.maze_buff_id, 2)

    def wiki(self) -> str:
        rogue_buffs = list(self.rogue_buffs())
        rogue_buffs.sort(key=lambda buff: buff.level)
        rogue_degrade = None
        rogue_upgrade = None
        if len(rogue_buffs) >= 1:
            rogue_degrade = rogue_buffs[0]
        if len(rogue_buffs) >= 2:
            rogue_upgrade = rogue_buffs[1]
        modes = ["差分宇宙"] if len(rogue_buffs) == 0 else ["模拟宇宙", "差分宇宙"]
        tourn_mode = next((group.mode for group in self.__rogue_tourn_buff_group if group.mode is not None), None)
        typ = None
        match self.category:
            case rogue.BuffCategory.Common:
                typ = 6
            case rogue.BuffCategory.Rare:
                typ = 5
            case rogue.BuffCategory.Legendary:
                typ = 3
            case None:
                typ = None
        return self._game._template_environment.get_template("祝福.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            name=self.wiki_name,
            category=self.category,
            buff_type=self.__rogue_tourn_buff_type.name,
            rogue_degrade=rogue_degrade,
            rogue_upgrade=rogue_upgrade,
            tourn_degrade=self.__degrade,
            tourn_upgrade=self.__upgrade,
            modes=modes,
            tourn_mode=tourn_mode,
            typ=typ,
        )


class RogueTournBuffGroup(View[excel.RogueTournBuffGroup]):
    ExcelOutput: typing.Final = excel.RogueTournBuffGroup

    @property
    def id(self) -> int:
        return self._excel.rogue_buff_group_id

    @property
    def rogue_buff_drop(self) -> list[int]:
        return self._excel.rogue_buff_drop

    @property
    def mode(self) -> rogue_tourn.Mode | None:
        return self._excel.tourn_mode

    @functools.cached_property
    def __drops(self) -> list[RogueTournBuff]:
        drops: list[RogueTournBuff] = []
        for drop in self.rogue_buff_drop:
            buff = self._game.rogue_tourn_buff_tag_buff(drop)
            if buff is None:
                continue
            drops.append(buff)
        return drops

    def drops(self) -> collections.abc.Iterable[RogueTournBuff]:
        return (RogueTournBuff(self._game, member._excel) for member in self.__drops)


class RogueTournBuffType(View[excel.RogueTournBuffType]):
    ExcelOutput: typing.Final = excel.RogueTournBuffType

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.rogue_buff_type_name)

    @functools.cached_property
    def title(self) -> str:
        return "" if self._excel.rogue_buff_type_title is None else self._game.text(self._excel.rogue_buff_type_title)

    @functools.cached_property
    def subtitle(self) -> str:
        return (
            ""
            if self._excel.rogue_buff_type_sub_title is None
            else self._game.text(self._excel.rogue_buff_type_sub_title)
        )


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

    def display(self) -> RogueTournFormulaDisplay:
        return RogueTournFormulaDisplay(self._game, self.__rogue_tourn_formula_display._excel)

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
        if self.__rogue_tourn_miracle_display.name != "":
            return self.__rogue_tourn_miracle_display.name
        return ""

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.name)  # pyright: ignore[reportPrivateUsage]

    @property
    def desc(self) -> str:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc
        return self.__rogue_tourn_miracle_display.desc

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc_param_list
        return self.__rogue_tourn_miracle_display.desc_param_list

    @property
    def category(self) -> rogue_tourn.MiracleCategory:
        return self._excel.miracle_category

    @property
    def mode(self) -> rogue_tourn.Mode:
        return self._excel.tourn_mode

    @property
    def bg_desc(self) -> str:
        return self.__rogue_tourn_miracle_display.bg_desc

    @property
    def tag(self) -> str:
        return self.__rogue_tourn_miracle_display.tag

    @functools.cached_property
    def __rogue_tourn_miracle_display(self) -> RogueMiracleDisplay:
        display = self._game.rogue_miracle_display(self._excel.miracle_display_id)
        if display is None:
            display = self._game.rogue_tourn_miracle_display(self._excel.miracle_display_id)
        assert display is not None
        return display

    def display(self) -> RogueMiracleDisplay:
        from .rogue import RogueMiracleDisplay

        return RogueMiracleDisplay(self._game, self.__rogue_tourn_miracle_display._excel)

    @functools.cached_property
    def __rogue_miracle_effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self._excel.miracle_effect_display_id is None:
            return None
        display = self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        assert display is not None
        return display

    def effect_display(self) -> RogueMiracleEffectDisplay | None:
        from .rogue import RogueMiracleEffectDisplay

        if self.__rogue_miracle_effect_display is None:
            return None
        return RogueMiracleEffectDisplay(self._game, self.__rogue_miracle_effect_display._excel)

    @functools.cached_property
    def __rogue_miracles(self) -> list[RogueMiracle]:
        return self._game.rogue_miracle_name(self.name)

    def rogue_miracles(self) -> list[RogueMiracle]:
        from .rogue import RogueMiracle

        return [RogueMiracle(self._game, miracle._excel) for miracle in self.__rogue_miracles]

    @functools.cached_property
    def __rogue_tourn_miracles(self) -> list[RogueTournMiracle]:
        return self._game.rogue_tourn_miracle_name(self.name)

    def tourn_miracles(self) -> list[RogueTournMiracle]:
        from .rogue_tourn import RogueTournMiracle

        return [RogueTournMiracle(self._game, miracle._excel) for miracle in self.__rogue_tourn_miracles]

    def wiki(self) -> str:
        modes = ["差分宇宙"] if len(self.__rogue_miracles) == 0 else ["模拟宇宙", "差分宇宙"]
        rogue_miracle = None if len(self.__rogue_miracles) == 0 else self.__rogue_miracles[-1]
        rogue_miracle_handbook = None if rogue_miracle is None else rogue_miracle.handbook()
        rogue_miracle_handbook_types = [] if rogue_miracle_handbook is None else list(rogue_miracle_handbook.types())
        tourn_miracles = self.tourn_miracles()
        tourn_miracles.sort(key=lambda miracle: miracle.mode)
        tourn_miracle = None if len(tourn_miracles) == 0 else tourn_miracles[-1]
        return self._game._template_environment.get_template("奇物.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            name=self.name,
            modes=modes,
            rogue_miracle=rogue_miracle,
            rogue_modes=rogue_miracle_handbook_types,
            tourn_miracle=tourn_miracle,
            tourn_modes=[miracle.mode for miracle in tourn_miracles],
        )


class RogueTournTitanBless(View[excel.RogueTournTitanBless]):
    ExcelOutput: typing.Final = excel.RogueTournTitanBless


class RogueTournWeeklyChallenge(View[excel.RogueTournWeeklyChallenge]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyChallenge


class RogueTournWeeklyDisplay(View[excel.RogueTournWeeklyDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyDisplay
