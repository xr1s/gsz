from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    from . import misc


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

    @functools.cached_property
    def name(self) -> str:
        return self.maze_buff.name

    @functools.cached_property
    def maze_buff(self) -> misc.MazeBuff:
        maze_buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        if maze_buff is None:
            maze_buff = self._game.maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert maze_buff is not None
        return maze_buff

    @functools.cached_property
    def type(self) -> RogueBuffType:
        typ = self._game.rogue_buff_type(self._excel.rogue_buff_type)
        assert typ is not None
        return typ


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

    @functools.cached_property
    def display(self) -> RogueMiracleDisplay | None:
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
    def effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self._excel.miracle_effect_display_id is None:
            return None
        display = self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def handbook(self) -> RogueHandbookMiracle | None:
        if self._excel.unlock_handbook_miracle_id is None:
            return None
        handbook = self._game.rogue_handbook_miracle(self._excel.unlock_handbook_miracle_id)
        assert handbook is not None
        return handbook

    @property
    def name(self) -> str:
        if self.display is not None:
            return self.display.name
        return ""

    @property
    def desc(self) -> str:
        if self.effect_display is not None:
            return self.effect_display.desc
        if self.display is not None:
            return self.display.desc
        return ""

    @property
    def simple_desc(self) -> str:
        if self.effect_display is not None:
            return self.effect_display.simple_desc
        return ""

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.effect_display is not None:
            return self.effect_display.desc_param_list
        if self.display is not None:
            return self.display.desc_param_list
        return ()


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
