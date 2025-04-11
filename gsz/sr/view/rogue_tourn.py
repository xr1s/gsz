from __future__ import annotations
import datetime
import functools
import itertools
import typing

from .. import excel
from ..excel import rogue, rogue_tourn
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .act import Act, Dialogue
    from .misc import MazeBuff
    from .rogue import (
        RogueBonus,
        RogueBuff,
        RogueHandbookMiracle,
        RogueMiracle,
        RogueMiracleDisplay,
        RogueMiracleEffectDisplay,
        RogueMonster,
        RogueNPC,
    )


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
    def is_in_handbook(self) -> bool:
        return self._excel.is_in_handbook

    @property
    def tag(self) -> int:
        return self._excel.rogue_buff_tag

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, self._excel.maze_buff_level)
        assert buff is not None
        return buff

    def maze_buff(self) -> MazeBuff:
        from .misc import MazeBuff

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
        groups = self._game._rogue_tourn_buff_tag_groups.get(self.tag)  # pyright: ignore[reportPrivateUsage]
        if groups is None:
            return []
        return [RogueTournBuffGroup(self._game, group) for group in groups]

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
            buff = self._game._rogue_tourn_buff_tag_buff.get(drop)  # pyright: ignore[reportPrivateUsage]
            if buff is None:
                continue
            drops.append(RogueTournBuff(self._game, buff))
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
        return self.__maze_buff.name

    @functools.cached_property
    def wiki_name(self) -> str:
        name = self._game._mw_formatter.format(self.name)  # pyright: ignore[reportPrivateUsage]
        if self.category == rogue_tourn.FormulaCategory.PathEcho and self.mode == rogue_tourn.Mode.TournMode1:
            return name + "（方程）"
        if self.name in ("赏金猎人", "混沌医师"):
            return name + "（方程）"
        return name

    @property
    def desc(self) -> str:
        """效果"""
        return self.__maze_buff.desc

    @property
    def category(self) -> rogue_tourn.FormulaCategory:
        """稀有度"""
        return self._excel.formula_category

    @property
    def param_list(self) -> tuple[float, ...]:
        return self.__maze_buff.param_list

    @property
    def mode(self) -> rogue_tourn.Mode | None:
        """
        人间喜剧、千面英雄
        None 应该是测试数据，观察到 None 里有一些重复的数据
        """
        return self._excel.tourn_mode

    @functools.cached_property
    def __main_buff_type(self) -> RogueTournBuffType:
        buff_type = self._game.rogue_tourn_buff_type(self._excel.main_buff_type_id)
        assert buff_type is not None
        return buff_type

    @property
    def main_buff_num(self) -> int:
        return self._excel.main_buff_num

    def main_buff_type(self) -> RogueTournBuffType:
        return RogueTournBuffType(self._game, self.__main_buff_type._excel)

    @functools.cached_property
    def __sub_buff_type(self) -> RogueTournBuffType | None:
        if self._excel.sub_buff_type_id is None:
            return None
        buff_type = self._game.rogue_tourn_buff_type(self._excel.sub_buff_type_id)
        assert buff_type is not None
        return buff_type

    def sub_buff_type(self) -> RogueTournBuffType | None:
        return None if self.__sub_buff_type is None else RogueTournBuffType(self._game, self.__sub_buff_type._excel)

    @property
    def sub_buff_num(self) -> int | None:
        return self._excel.sub_buff_num

    @functools.cached_property
    def __rogue_tourn_formula_display(self) -> RogueTournFormulaDisplay:
        display = self._game.rogue_tourn_formula_display(self._excel.formula_display_id)
        assert display is not None
        return display

    def display(self) -> RogueTournFormulaDisplay:
        """方程效果和演绎"""
        return RogueTournFormulaDisplay(self._game, self.__rogue_tourn_formula_display._excel)

    @functools.cached_property
    def __story(self) -> Act | None:
        from .act import Act

        if self._game.base.joinpath(self._excel.formula_story_json).is_file():
            return Act(self._game, self._excel.formula_story_json)
        return None

    def story(self) -> Act | None:
        """推演"""
        from .act import Act

        return None if self.__story is None else Act(self._game, self.__story._act)  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        maze_buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, 1)
        assert maze_buff is not None
        return maze_buff

    def maze_buff(self) -> MazeBuff:
        from .misc import MazeBuff

        return MazeBuff(self._game, self.__maze_buff._excel)

    def wiki(self) -> str:
        return self._game._template_environment.get_template("差分宇宙方程.jinja2").render(formula=self)  # pyright: ignore[reportPrivateUsage]


class RogueTournFormulaDisplay(View[excel.RogueTournFormulaDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournFormulaDisplay

    @functools.cached_property
    def story(self) -> str:
        return self._game.text(self._excel.formula_story)


class RogueTournHandBookEvent(View[excel.RogueTournHandBookEvent]):
    ExcelOutput: typing.Final = excel.RogueTournHandBookEvent

    @property
    def name(self) -> str:
        return self.title

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.event_title)

    @functools.cached_property
    def __npcs(self) -> list[RogueNPC]:
        npcs: list[RogueNPC] = []
        for npc_progress_id in self._excel.unlock_npc_progress_id_list:
            npc = self._game.rogue_tourn_npc(npc_progress_id.unlock_npc_id)
            assert npc is not None
            npcs.append(npc)
        return npcs

    def npcs(self) -> collections.abc.Iterable[RogueNPC]:
        from .rogue import RogueNPC

        return (RogueNPC(self._game, npc._excel) for npc in self.__npcs)

    @functools.cached_property
    def __dialogues(self) -> list[Dialogue]:
        dialogues: list[Dialogue] = []
        for prog_id, npc in zip(self._excel.unlock_npc_progress_id_list, self.__npcs, strict=True):
            dialogue = next(
                dialogue for dialogue in npc.dialogue_list() if dialogue.progress == prog_id.unlock_progress
            )
            dialogues.append(dialogue)
        return dialogues

    def dialogues(self) -> collections.abc.Iterable[Dialogue]:
        from .act import Dialogue

        return (Dialogue(self._game, dialogue._dialogue) for dialogue in self.__dialogues)  # pyright: ignore[reportPrivateUsage]


class RogueTournHandbookMiracle(View[excel.RogueTournHandbookMiracle]):
    ExcelOutput: typing.Final = excel.RogueTournHandbookMiracle

    @property
    def name(self) -> str:
        return self.__rogue_tourn_miracle_display.name

    @property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.__rogue_tourn_miracle_display.name.replace("#", "＃"))  # pyright: ignore[reportPrivateUsage]

    @property
    def desc(self) -> str:
        if self.__rogue_tourn_miracle_effect_display is not None:
            return self.__rogue_tourn_miracle_effect_display.desc
        return self.__rogue_tourn_miracle_display.desc

    @property
    def desc_param_list(self) -> tuple[float, ...]:
        if self.__rogue_tourn_miracle_effect_display is not None:
            return self.__rogue_tourn_miracle_effect_display.desc_param_list
        return self.__rogue_tourn_miracle_display.desc_param_list

    @property
    def bg_desc(self) -> str:
        return self.__rogue_tourn_miracle_display.bg_desc

    @property
    def category(self) -> rogue_tourn.MiracleCategory:
        return self._excel.miracle_category

    @functools.cached_property
    def __rogue_tourn_miracle_display(self) -> RogueMiracleDisplay:
        display = self._game.rogue_miracle_display(self._excel.miracle_display_id)
        if display is None:
            display = self._game.rogue_tourn_miracle_display(self._excel.miracle_display_id)
        assert display is not None
        return display

    @functools.cached_property
    def __rogue_tourn_miracle_effect_display(self) -> RogueMiracleEffectDisplay | None:
        return (
            None
            if self._excel.miracle_effect_display_id is None
            else self._game.rogue_miracle_effect_display(self._excel.miracle_effect_display_id)
        )

    @functools.cached_property
    def __rogue_handbook_miracle(self) -> RogueHandbookMiracle | None:
        handbook = self._game.rogue_handbook_miracle_name(self.name)
        assert len(handbook) in (0, 1)
        return None if len(handbook) == 0 else handbook[0]

    @functools.cached_property
    def __rogue_tourn_miracles(self) -> list[RogueTournMiracle]:
        miracles = self._game._rogue_tourn_handbook_miracle_miracles.get(self._excel.id)  # pyright: ignore[reportPrivateUsage]
        if miracles is None:
            return []
        return [RogueTournMiracle(self._game, miracle) for miracle in miracles]

    @functools.cached_property
    def __same_name_rogue_tourn_miracles(self) -> list[RogueTournMiracle]:
        return self._game.rogue_tourn_miracle_name(self.name)

    def tourn_miracles(self) -> collections.abc.Iterable[RogueTournMiracle]:
        return (RogueTournMiracle(self._game, miracle._excel) for miracle in self.__rogue_tourn_miracles)

    def wiki(self) -> str:
        handbooks = [
            handbook
            for handbook in self._game.rogue_tourn_handbook_miracle_name(self.name)
            if len(handbook.__rogue_tourn_miracles) != 0
        ]
        if len(handbooks) == 0:
            return ""
        handbook = handbooks[-1]
        modes = ["差分宇宙"] if self.__rogue_handbook_miracle is None else ["模拟宇宙", "差分宇宙"]
        rogue_miracle_handbook_types = (
            []
            if self.__rogue_handbook_miracle is None
            else [typ.title.removeprefix("模拟宇宙：") for typ in self.__rogue_handbook_miracle.types()]
        )
        tourn_modes = list({miracle.mode for miracle in self.__same_name_rogue_tourn_miracles})
        tourn_modes.sort()
        return self._game._template_environment.get_template("奇物.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            name=handbook.wiki_name,
            modes=modes,
            rogue_miracle=self.__rogue_handbook_miracle,
            rogue_modes=rogue_miracle_handbook_types,
            tourn_miracle=handbook,
            tourn_modes=tourn_modes,
        )


class RogueTournMiracle(View[excel.RogueTournMiracle]):
    ExcelOutput: typing.Final = excel.RogueTournMiracle

    @property
    def name(self) -> str:
        if self.__rogue_tourn_miracle_display.name != "":
            return self.__rogue_tourn_miracle_display.name
        return ""

    @functools.cached_property
    def wiki_name(self) -> str:
        return self._game._mw_formatter.format(self.name.replace("#", "＃"))  # pyright: ignore[reportPrivateUsage]

    @property
    def desc(self) -> str:
        """效果"""
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
        """稀有度"""
        return self._excel.miracle_category

    @property
    def mode(self) -> rogue_tourn.Mode:
        """人间喜剧、千面英雄"""
        return self._excel.tourn_mode

    @property
    def bg_desc(self) -> str:
        """背景故事"""
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
        """奇物名称、效果、背景故事等字段"""
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
        """新版奇物效果字段，取代 RogueMiracleDisplay"""
        from .rogue import RogueMiracleEffectDisplay

        if self.__rogue_miracle_effect_display is None:
            return None
        return RogueMiracleEffectDisplay(self._game, self.__rogue_miracle_effect_display._excel)

    @functools.cached_property
    def __same_name_rogue_miracles(self) -> list[RogueMiracle]:
        return self._game.rogue_miracle_name(self.name)

    def same_name_rogue_miracles(self) -> collections.abc.Iterable[RogueMiracle]:
        """同名模拟宇宙奇物"""
        from .rogue import RogueMiracle

        return (RogueMiracle(self._game, miracle._excel) for miracle in self.__same_name_rogue_miracles)

    @functools.cached_property
    def __same_name_rogue_tourn_miracles(self) -> list[RogueTournMiracle]:
        return self._game.rogue_tourn_miracle_name(self.name)

    def same_name_tourn_miracles(self) -> collections.abc.Iterable[RogueTournMiracle]:
        """同名差分宇宙奇物"""
        from .rogue_tourn import RogueTournMiracle

        return [RogueTournMiracle(self._game, miracle._excel) for miracle in self.__same_name_rogue_tourn_miracles]


class RogueTournTitanBless(View[excel.RogueTournTitanBless]):
    ExcelOutput: typing.Final = excel.RogueTournTitanBless

    @property
    def name(self) -> str:
        return self.__maze_buff.name

    @property
    def wiki_name(self) -> str:
        return self.__maze_buff.name

    @property
    def titan_type(self) -> rogue_tourn.TitanType:
        return self._excel.titan_type

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        buff = self._game.rogue_maze_buff(self._excel.maze_buff_id, 1)
        assert buff is not None
        return buff

    def maze_buff(self) -> MazeBuff:
        from .misc import MazeBuff

        return MazeBuff(self._game, self.__maze_buff._excel)


class RogueTournWeeklyChallenge(View[excel.RogueTournWeeklyChallenge]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyChallenge

    @property
    def id(self) -> int:
        return self._excel.challenge_id

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.weekly_name)

    ASIA_SHANGHAI: datetime.timezone = datetime.timezone(datetime.timedelta(hours=8))
    FIRST_CHALLENGE_MONDAY: datetime.datetime = datetime.datetime(2024, 6, 17, 4, tzinfo=ASIA_SHANGHAI)

    @functools.cached_property
    def __begin_time(self) -> datetime.datetime:
        if self.id == 1:
            return self.FIRST_CHALLENGE_MONDAY + datetime.timedelta(days=2, hours=7)
        return self.FIRST_CHALLENGE_MONDAY + datetime.timedelta(weeks=self.id - 1)

    def begin_time(self) -> datetime.datetime:
        return self.__begin_time

    def begin_date(self) -> datetime.date:
        return self.__begin_time.date()

    @functools.cached_property
    def __end_time(self) -> datetime.datetime:
        return self.FIRST_CHALLENGE_MONDAY + datetime.timedelta(weeks=self.id, milliseconds=-1)

    def end_time(self) -> datetime.datetime:
        return self.__end_time

    def end_date(self) -> datetime.date:
        return self.__end_time.date() - datetime.timedelta(days=1)

    @functools.cached_property
    def __contents(self) -> list[RogueTournWeeklyDisplay]:
        return list(self._game.rogue_tourn_weekly_display(self._excel.weekly_content_list))

    def contents(self) -> collections.abc.Iterable[RogueTournWeeklyDisplay]:
        return (RogueTournWeeklyDisplay(self._game, display._excel) for display in self.__contents)

    @functools.cached_property
    def __details(self) -> list[RogueTournWeeklyDisplay]:
        # 几个不存在的值，据观察不存在直接没展示
        weekly_content_detail_list = (
            detail for detail in self._excel.weekly_content_detail_list if detail not in (1302, 1303)
        )
        return list(self._game.rogue_tourn_weekly_display(weekly_content_detail_list))

    def details(self) -> collections.abc.Iterable[RogueTournWeeklyDisplay]:
        return (RogueTournWeeklyDisplay(self._game, display._excel) for display in self.__details)

    def miracles(self) -> list[RogueTournMiracle]:
        return list(itertools.chain.from_iterable(content.miracles() for content in self.__contents))

    def formulas(self) -> list[RogueTournFormula]:
        return list(itertools.chain.from_iterable(content.formulas() for content in self.__contents))

    def titan_blesses(self) -> list[RogueTournTitanBless]:
        return list(itertools.chain.from_iterable(content.titan_blesses() for content in self.__contents))

    def __find_bonus(self, bonus_start: int, challenge_start: int) -> RogueBonus:
        bonus = self._game.rogue_bonus(bonus_start)
        assert bonus is not None
        for challenge in self._game.rogue_tourn_weekly_challenge(range(challenge_start + 1, self.id + 1)):
            if len(challenge.formulas()) == 0:
                continue
            bonus = self._game.rogue_bonus(bonus.id + 1)
            assert bonus is not None
            while not bonus.desc.startswith("获得一些"):
                bonus = self._game.rogue_bonus(bonus.id + 1)
                assert bonus is not None
        return bonus

    @functools.cached_property
    def __bonus(self) -> RogueBonus | None:
        if len(self.formulas()) == 0:
            return None
        if self.id <= 37:  # 人间喜剧
            return self.__find_bonus(410, 1)
        # 千面英雄
        return self.__find_bonus(504, 38)

    def bonus(self) -> RogueBonus | None:
        from .rogue import RogueBonus

        return None if self.__bonus is None else RogueBonus(self._game, self.__bonus._excel)

    @functools.cached_property
    def __monster_1st_plain(self) -> list[RogueMonster]:
        monster_group_id = self._excel.display_monster_groups_1["0"]
        monster_group = self._game.rogue_monster_group(monster_group_id)
        assert monster_group is not None
        return monster_group.monsters()

    def monster_1st_plain(self) -> collections.abc.Iterable[RogueMonster]:
        from .rogue import RogueMonster

        return (RogueMonster(self._game, monster._excel) for monster in self.__monster_1st_plain)

    @functools.cached_property
    def __monster_1st_plain_v3(self) -> list[RogueMonster]:
        monster_group_id = self._excel.display_monster_groups_1["3"]
        monster_group = self._game.rogue_monster_group(monster_group_id)
        assert monster_group is not None
        return monster_group.monsters()

    def monster_1st_plain_v3(self) -> collections.abc.Iterable[RogueMonster]:
        from .rogue import RogueMonster

        return (RogueMonster(self._game, monster._excel) for monster in self.__monster_1st_plain_v3)

    @functools.cached_property
    def __monster_2nd_plain(self) -> list[RogueMonster]:
        monster_group_id = self._excel.display_monster_groups_2["0"]
        monster_group = self._game.rogue_monster_group(monster_group_id)
        assert monster_group is not None
        return monster_group.monsters()

    def monster_2nd_plain(self) -> collections.abc.Iterable[RogueMonster]:
        from .rogue import RogueMonster

        return (RogueMonster(self._game, monster._excel) for monster in self.__monster_2nd_plain)

    @functools.cached_property
    def __monster_2nd_plain_v3(self) -> list[RogueMonster]:
        monster_group_id = self._excel.display_monster_groups_2["3"]
        monster_group = self._game.rogue_monster_group(monster_group_id)
        assert monster_group is not None
        return monster_group.monsters()

    def monster_2nd_plain_v3(self) -> collections.abc.Iterable[RogueMonster]:
        from .rogue import RogueMonster

        return (RogueMonster(self._game, monster._excel) for monster in self.__monster_2nd_plain_v3)

    @functools.cached_property
    def __monster_3rd_plain(self) -> list[RogueMonster]:
        monster_group_id = self._excel.display_monster_groups_3["0"]
        monster_group = self._game.rogue_monster_group(monster_group_id)
        assert monster_group is not None
        return monster_group.monsters()

    def monster_3rd_plain(self) -> collections.abc.Iterable[RogueMonster]:
        from .rogue import RogueMonster

        return (RogueMonster(self._game, monster._excel) for monster in self.__monster_3rd_plain)

    def wiki(self) -> str:
        details = (detail.wiki_content.removeprefix("●") for detail in self.details())
        return self._game._template_environment.get_template("周期演算.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            challenge=self,
            miracles=list(self.miracles()),
            formulas=list(self.formulas()),
            titan_blesses=list(self.titan_blesses()),
            bonus=self.bonus(),
            details=details,
        )


class RogueTournWeeklyDisplay(View[excel.RogueTournWeeklyDisplay]):
    ExcelOutput: typing.Final = excel.RogueTournWeeklyDisplay

    @functools.cached_property
    def content(self) -> str:
        return self._game.text(self._excel.weekly_display_content)

    @functools.cached_property
    def __desc_params(self) -> list[RogueTournFormula | RogueTournMiracle | RogueTournTitanBless]:
        params: list[RogueTournFormula | RogueTournMiracle | RogueTournTitanBless] = []
        for param in self._excel.desc_params:
            match param.type:
                case rogue_tourn.DescParamType.Formula:
                    value = self._game.rogue_tourn_formula(param.value)
                    assert value is not None
                    params.append(value)
                case rogue_tourn.DescParamType.Miracle:
                    value = self._game.rogue_tourn_miracle(param.value)
                    assert value is not None
                    params.append(value)
                case rogue_tourn.DescParamType.TitanBless:
                    value = self._game.rogue_tourn_titan_bless(param.value)
                    assert value is not None
                    params.append(value)
        return params

    @functools.cached_property
    def wiki_content(self) -> str:
        desc_params = [param.wiki_name for param in self.__desc_params]
        return self._game._mw_formatter.format(self.content, desc_params)  # pyright: ignore[reportPrivateUsage]

    @functools.cached_property
    def __miracles(self) -> list[RogueTournMiracle]:
        miracle_ids = [
            param.value
            for param in self._excel.desc_params
            if param.type == rogue_tourn.DescParamType.Miracle
            if param.value not in (6907, 6908)  # 3.1 疑似缺数据
        ]
        return list(self._game.rogue_tourn_miracle(miracle_ids))

    def miracles(self) -> collections.abc.Iterable[RogueTournMiracle]:
        return (RogueTournMiracle(self._game, miracle._excel) for miracle in self.__miracles)

    @functools.cached_property
    def __formulas(self) -> list[RogueTournFormula]:
        formula_ids = [
            param.value for param in self._excel.desc_params if param.type == rogue_tourn.DescParamType.Formula
        ]
        return list(self._game.rogue_tourn_formula(formula_ids))

    def formulas(self) -> collections.abc.Iterable[RogueTournFormula]:
        return (RogueTournFormula(self._game, formula._excel) for formula in self.__formulas)

    @functools.cached_property
    def __titan_blesses(self) -> list[RogueTournTitanBless]:
        titan_blessing_ids = [
            param.value for param in self._excel.desc_params if param.type == rogue_tourn.DescParamType.TitanBless
        ]
        return list(self._game.rogue_tourn_titan_bless(titan_blessing_ids))

    def titan_blesses(self) -> collections.abc.Iterable[RogueTournTitanBless]:
        return (RogueTournTitanBless(self._game, titan_bless._excel) for titan_bless in self.__titan_blesses)
