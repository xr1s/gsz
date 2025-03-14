from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from . import misc
    from .rogue_tourn import RogueTournMiracle


class RogueBonus(View[excel.RogueBonus]):
    ExcelOutput: typing.Final = excel.RogueBonus

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.bonus_title)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.bonus_desc)


class RogueBuff(View[excel.RogueBuff]):
    ExcelOutput: typing.Final = excel.RogueBuff

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
    def __maze_buff(self) -> misc.MazeBuff:
        maze_buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        if maze_buff is None:
            maze_buff = self._game.maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert maze_buff is not None
        return maze_buff

    @functools.cached_property
    def __type(self) -> RogueBuffType:
        typ = self._game.rogue_buff_type(self._excel.rogue_buff_type)
        assert typ is not None
        return typ

    def wiki(self) -> str:
        return self._game._template_environment.get_template("祝福.jinja2").render(buff=self)  # pyright: ignore[reportPrivateUsage]


class RogueBuffType(View[excel.RogueBuffType]):
    ExcelOutput: typing.Final = excel.RogueBuffType

    @functools.cached_property
    def text(self) -> str:
        return self._game.text(self._excel.rogue_buff_type_textmap_id)

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.rogue_buff_type_title)

    @functools.cached_property
    def subtitle(self) -> str:
        if self._excel.rogue_buff_type_sub_title is None:
            return ""
        return self._game.text(self._excel.rogue_buff_type_sub_title)


class RogueHandbookMiracle(View[excel.RogueHandbookMiracle]):
    ExcelOutput: typing.Final = excel.RogueHandbookMiracle


class RogueHandbookMiracleType(View[excel.RogueHandbookMiracleType]):
    ExcelOutput: typing.Final = excel.RogueHandbookMiracleType


class RogueMiracle(View[excel.RogueMiracle]):
    ExcelOutput: typing.Final = excel.RogueMiracle

    @property
    def name(self) -> str:
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.name
        return ""

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.name)  # pyright: ignore[reportPrivateUsage]

    @property
    def desc(self) -> str:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc
        return ""

    @property
    def simple_desc(self) -> str:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.simple_desc
        return ""

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc_param_list
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc_param_list
        return ()

    @property
    def bg_desc(self) -> str:
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.bg_desc
        return ""

    @property
    def tag(self) -> str:
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.tag
        return ""

    @functools.cached_property
    def __rogue_tourn_miracle(self) -> RogueTournMiracle | None:
        return self._game.rogue_tourn_miracle_name(self.name)

    def rogue_tourn(self) -> RogueTournMiracle | None:
        from .rogue_tourn import RogueTournMiracle

        if self.__rogue_tourn_miracle is not None:
            return RogueTournMiracle(self._game, self.__rogue_tourn_miracle._excel)
        return None

    @functools.cached_property
    def __rogue_miracle_display(self) -> RogueMiracleDisplay | None:
        if self._excel.miracle_display_id is None:
            # 兼容 1.2 老数据
            if self._excel.miracle_name is None:
                return None
            assert self._excel.miracle_name is not None
            assert self._excel.miracle_icon_path is not None
            assert self._excel.miracle_figure_icon_path is not None
            display = excel.RogueMiracleDisplay(
                miracle_display_id=0,
                miracle_name=self._excel.miracle_name,
                miracle_desc=self._excel.miracle_desc,
                desc_param_list=self._excel.desc_param_list,
                extra_effect=self._excel.extra_effect,
                miracle_bg_desc=self._excel.miracle_bg_desc,
                miracle_tag=self._excel.miracle_tag,
                miracle_icon_path=self._excel.miracle_icon_path,
                miracle_figure_icon_path=self._excel.miracle_figure_icon_path,
            )
            return RogueMiracleDisplay(game=self._game, excel=display)
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

    def display(self) -> RogueMiracleDisplay | None:
        if self.__rogue_miracle_display is None:
            return None
        return RogueMiracleDisplay(self._game, self.__rogue_miracle_display._excel)

    def effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self.__rogue_miracle_effect_display is None:
            return None
        return RogueMiracleEffectDisplay(self._game, self.__rogue_miracle_effect_display._excel)

    @functools.cached_property
    def __rogue_handbook_miracle(self) -> RogueHandbookMiracle | None:
        if self._excel.unlock_handbook_miracle_id is None:
            return None
        handbook = self._game.rogue_handbook_miracle(self._excel.unlock_handbook_miracle_id)
        assert handbook is not None
        return handbook

    def handbook(self) -> RogueHandbookMiracle | None:
        if self.__rogue_handbook_miracle is None:
            return None
        return RogueHandbookMiracle(self._game, self.__rogue_handbook_miracle._excel)

    def wiki(self) -> str:
        modes = ["模拟宇宙"] if self.__rogue_tourn_miracle is None else ["模拟宇宙", "差分宇宙"]
        return self._game._template_environment.get_template("奇物.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            miracle=self, tourn_miracle=self.__rogue_tourn_miracle, modes=modes
        )


class RogueMiracleDisplay(View[excel.RogueMiracleDisplay]):
    ExcelOutput: typing.Final = excel.RogueMiracleDisplay

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.miracle_name)

    @functools.cached_property
    def desc(self) -> str:
        if self._excel.miracle_desc is None:
            return ""
        return self._game.text(self._excel.miracle_desc)

    @functools.cached_property
    def desc_param_list(self) -> tuple[float, ...]:
        if self._excel.desc_param_list is None:
            return ()
        return tuple(param.value for param in self._excel.desc_param_list)

    @functools.cached_property
    def bg_desc(self) -> str:
        if self._excel.miracle_bg_desc is None:
            return ""
        return self._game.text(self._excel.miracle_bg_desc)

    @functools.cached_property
    def tag(self) -> str:
        if self._excel.miracle_tag is None:
            return ""
        return self._game.text(self._excel.miracle_tag)


class RogueMiracleEffectDisplay(View[excel.RogueMiracleEffectDisplay]):
    ExcelOutput: typing.Final = excel.RogueMiracleEffectDisplay

    @functools.cached_property
    def desc(self) -> str:
        if self._excel.miracle_desc is None:
            return ""
        return self._game.text(self._excel.miracle_desc)

    @functools.cached_property
    def simple_desc(self) -> str:
        if self._excel.miracle_simple_desc is None:
            return ""
        return self._game.text(self._excel.miracle_simple_desc)

    @functools.cached_property
    def desc_param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.desc_param_list)


class RogueMonster(View[excel.RogueMonster]):
    ExcelOutput: typing.Final = excel.RogueMonster


class RogueMonsterGroup(View[excel.RogueMonsterGroup]):
    ExcelOutput: typing.Final = excel.RogueMonsterGroup
