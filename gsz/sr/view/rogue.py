from __future__ import annotations
import functools
import itertools
import typing

from .. import excel
from ..excel import rogue
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc
    from . import misc
    from .rogue_tourn import RogueTournMiracle, RogueTournBuff, RogueTournHandbookMiracle


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
    def tag(self) -> int:
        return self._excel.rogue_buff_tag

    @functools.cached_property
    def __maze_buff(self) -> misc.MazeBuff:
        maze_buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        if maze_buff is None:
            maze_buff = self._game.maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert maze_buff is not None
        return maze_buff

    def maze_buff(self) -> misc.MazeBuff:
        from .misc import MazeBuff

        return MazeBuff(self._game, self.__maze_buff._excel)

    @functools.cached_property
    def __rogue_buff_group(self) -> list[RogueBuffGroup]:
        return self._game.rogue_buff_tag_groups(self.tag)

    @functools.cached_property
    def __tag_drops(self) -> list[RogueBuff]:
        return list(itertools.chain.from_iterable(group.drops() for group in self.__rogue_buff_group))

    @functools.cached_property
    def tag_drops(self) -> collections.abc.Iterable[RogueBuff]:
        return [RogueBuff(self._game, member._excel) for member in self.__tag_drops]

    @functools.cached_property
    def __rogue_buff_type(self) -> RogueBuffType:
        typ = self._game.rogue_buff_type(self._excel.rogue_buff_type)
        assert typ is not None
        return typ

    def type(self) -> RogueBuffType:
        return RogueBuffType(self._game, self.__rogue_buff_type._excel)

    @functools.cached_property
    def __rogue_tourn_buffs(self) -> list[RogueTournBuff]:
        return list(self._game.rogue_tourn_buff_name(self.name))

    def tourn_buffs(self) -> collections.abc.Iterable[RogueTournBuff]:
        from .rogue_tourn import RogueTournBuff

        return (RogueTournBuff(self._game, buff._excel) for buff in self.__rogue_tourn_buffs)

    @property
    def category(self) -> rogue.BuffCategory | None:
        if self._excel.rogue_buff_category is not None:
            return self._excel.rogue_buff_category
        match self._excel.rogue_buff_rarity:
            case 1:
                return rogue.BuffCategory.Common
            case 2:
                return rogue.BuffCategory.Rare
            case 3 | 4:
                return rogue.BuffCategory.Legendary
            case None:
                return None  # 无尽活动存在无稀有度祝福

    @functools.cached_property
    def __upgrade(self) -> RogueBuff | None:
        if self.__maze_buff.level_max == 1:
            return None
        if self._excel.maze_buff_level == 2:
            return self
        return self._game.rogue_buff(self._excel.maze_buff_id, 2)

    def upgrade(self) -> RogueBuff | None:
        return None if self.__upgrade is None else RogueBuff(self._game, self.__upgrade._excel)

    @functools.cached_property
    def __degrade(self) -> RogueBuff:
        if self._excel.maze_buff_level == 1:
            return self
        buff = self._game.rogue_buff(self._excel.maze_buff_id, 1)
        assert buff is not None
        return buff

    def degrade(self) -> RogueBuff:
        return RogueBuff(self._game, self.__degrade._excel)

    def wiki(self) -> str:
        tourn_buffs = list(self.tourn_buffs())
        tourn_buffs.sort(key=lambda buff: buff.level)
        tourn_degrade = None
        tourn_upgrade = None
        if len(tourn_buffs) >= 1:
            tourn_degrade = tourn_buffs[0]
        if len(tourn_buffs) >= 2:
            tourn_upgrade = tourn_buffs[1]
        modes = ["模拟宇宙"] if len(tourn_buffs) == 0 else ["模拟宇宙", "差分宇宙"]
        typ = None
        match self.category:
            case rogue.BuffCategory.Common:
                typ = 6
            case rogue.BuffCategory.Rare:
                typ = 5
            case rogue.BuffCategory.Legendary:
                typ = 4
                if self.name.startswith("命途回响"):
                    typ = 1
                if self.name.startswith("回响构音"):
                    typ = 2
                if self.name.startswith("回响交错"):
                    typ = 3
            case None:
                typ = None
        return self._game._template_environment.get_template("祝福.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            name=self.wiki_name,
            category=self.category,
            buff_type=self.__rogue_buff_type.subtitle,
            rogue_degrade=self.__degrade,
            rogue_upgrade=self.__upgrade,
            tourn_degrade=tourn_upgrade,
            tourn_upgrade=tourn_degrade,
            modes=modes,
            typ=typ,
        )


class RogueBuffGroup(View[excel.RogueBuffGroup]):
    ExcelOutput: typing.Final = excel.RogueBuffGroup

    @property
    def id(self) -> int:
        return self._excel.id

    @property
    def rogue_buff_drop(self) -> list[int]:
        return self._excel.rogue_buff_drop

    @functools.cached_property
    def __drops(self) -> list[RogueBuff]:
        members: list[RogueBuff] = []
        for member_tag in self.rogue_buff_drop:
            buff = self._game.rogue_buff_tag_buff(member_tag)
            if buff is None:
                continue
            members.append(buff)
        return members

    def drops(self) -> collections.abc.Iterable[RogueBuff]:
        return (RogueBuff(self._game, member._excel) for member in self.__drops)


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

    @property
    def name(self) -> str:
        if self.__rogue_magic_miracle is not None:
            return self.__rogue_magic_miracle.name
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
        if self.__rogue_magic_miracle is not None:
            return self.__rogue_magic_miracle.desc
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc
        return ""

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc_param_list
        if self.__rogue_magic_miracle is not None:
            return self.__rogue_magic_miracle.desc_param_list
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc_param_list
        return ()

    @property
    def bg_desc(self) -> str:
        if self.__rogue_magic_miracle is not None:
            return self.__rogue_magic_miracle.bg_desc
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.bg_desc
        return ""

    @functools.cached_property
    def __rogue_handbook_miracle_type(self) -> list[RogueHandbookMiracleType]:
        return list(self._game.rogue_handbook_miracle_type(self._excel.miracle_type_list))

    @functools.cached_property
    def __rogue_magic_miracle(self) -> RogueMiracle | None:
        if self._excel.miracle_id_for_effect_display is None:
            return None
        miracle = self._game.rogue_magic_miracle(self._excel.miracle_id_for_effect_display)
        assert miracle is not None
        return miracle

    def types(self) -> collections.abc.Iterable[RogueHandbookMiracleType]:
        return (RogueHandbookMiracleType(self._game, typ._excel) for typ in self.__rogue_handbook_miracle_type)

    @functools.cached_property
    def __rogue_miracle_display(self) -> RogueMiracleDisplay | None:
        # 不可知域 2.7 ~ 3.0 版本的奇物都没有正确的 RogueMiracleDisplay，索引到 RogueTournMiracleDisplay 去了
        display = self._game.rogue_miracle_display(self._excel.miracle_display_id)
        if display is None:
            display = self._game.rogue_tourn_miracle_display(self._excel.miracle_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def __rogue_miracle_effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self._excel.miracle_effect_display_id is None:
            return None
        display = self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def __rogue_miracles(self) -> list[RogueMiracle]:
        return list(self._game.rogue_handbook_miracle_miracles(self._excel.id))

    def rogue_miracles(self) -> collections.abc.Iterable[RogueMiracle]:
        return (RogueMiracle(self._game, miracle._excel) for miracle in self.__rogue_miracles)

    @functools.cached_property
    def __rogue_tourn_handbook_miracle(self) -> RogueTournHandbookMiracle | None:
        handbook = [
            handbook
            for handbook in self._game.rogue_tourn_handbook_miracle_name(self.name)
            if len(list(handbook.tourn_miracles())) != 0
        ]
        return None if len(handbook) == 0 else handbook[-1]

    @functools.cached_property
    def __same_name_rogue_tourn_miracles(self) -> list[RogueTournMiracle]:
        return self._game.rogue_tourn_miracle_name(self.name)

    def wiki(self) -> str:
        modes = ["模拟宇宙"] if len(self.__same_name_rogue_tourn_miracles) == 0 else ["模拟宇宙", "差分宇宙"]
        rogue_modes = [typ.title.removeprefix("模拟宇宙：") for typ in self.__rogue_handbook_miracle_type]
        tourn_modes = list({miracle.mode for miracle in self.__same_name_rogue_tourn_miracles})
        tourn_modes.sort()
        return self._game._template_environment.get_template("奇物.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            name=self.wiki_name,
            modes=modes,
            rogue_miracle=self,
            rogue_modes=rogue_modes,
            tourn_miracle=self.__rogue_tourn_handbook_miracle,
            tourn_modes=tourn_modes,
        )


class RogueHandbookMiracleType(View[excel.RogueHandbookMiracleType]):
    ExcelOutput: typing.Final = excel.RogueHandbookMiracleType

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.rogue_miracle_type_title)


class RogueMiracle(View[excel.RogueMiracle]):
    ExcelOutput: typing.Final = excel.RogueMiracle

    @functools.cached_property
    def name(self) -> str:
        if self._excel.miracle_name is not None:
            return self._game.text(self._excel.miracle_name)
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.name
        return ""

    @functools.cached_property
    def desc(self) -> str:
        if self._excel.miracle_desc is not None:
            desc = self._game.text(self._excel.miracle_desc)
            if desc != "":
                return desc
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc
        return ""

    @functools.cached_property
    def desc_param_list(self) -> tuple[float, ...]:
        if self._excel.desc_param_list is not None:
            return tuple(param.value for param in self._excel.desc_param_list)
        if self.__rogue_miracle_effect_display is not None:
            return self.__rogue_miracle_effect_display.desc_param_list
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.desc_param_list
        return ()

    @functools.cached_property
    def bg_desc(self) -> str:
        if self._excel.miracle_bg_desc is not None:
            return self._game.text(self._excel.miracle_bg_desc)
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.bg_desc
        return ""

    @property
    def tag(self) -> str:
        if self.__rogue_miracle_display is not None:
            return self.__rogue_miracle_display.tag
        return ""

    @functools.cached_property
    def __rogue_miracles(self) -> list[RogueMiracle]:
        return self._game.rogue_miracle_name(self.name)

    def rogue_miracles(self) -> collections.abc.Iterable[RogueMiracle]:
        return (RogueMiracle(self._game, miracle._excel) for miracle in self.__rogue_miracles)

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
        if display is None:
            display = self._game.rogue_tourn_miracle_display(self._excel.miracle_display_id)
        assert display is not None
        return display

    def display(self) -> RogueMiracleDisplay | None:
        if self.__rogue_miracle_display is None:
            return None
        return RogueMiracleDisplay(self._game, self.__rogue_miracle_display._excel)

    @functools.cached_property
    def __rogue_miracle_effect_display(self) -> RogueMiracleEffectDisplay | None:
        if self._excel.miracle_effect_display_id is None:
            return None
        display = self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        assert display is not None
        return display

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
