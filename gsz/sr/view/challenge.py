from __future__ import annotations

import functools
import typing

from .. import excel
from ..excel import Element, challenge
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .misc import MazeBuff, ScheduleData
    from .monster import HardLevelGroup, MonsterConfig, MonsterTemplateConfig
    from .stage import StageConfig


class SpecialMonster:
    """在逐光捡金中被全局 HardLevelGroup 修改属性敌方，只用来聚合数据，不暴露到外面"""

    def __init__(self, monster: MonsterConfig, hard_level_group: HardLevelGroup, floors: int):
        self.__monster = monster
        self.__hard_level_group = hard_level_group
        self.__proto = monster.prototype()
        template = monster.template()
        assert template is not None
        self.__template = template
        self.__floors = {floors}

    def append_floor(self, floor: int):
        self.__floors.add(floor)

    def floors(self) -> list[int]:
        floors = list(self.__floors)
        floors.sort()
        return floors

    @property
    def wiki_name(self) -> str:
        return self.__monster.wiki_name

    @functools.cached_property
    def __speed(self) -> float:
        return self.__hard_level_group.speed_ratio * (
            self.__template.speed_base * self.__monster.speed_modify_ratio + self.__monster.speed_modify_value
        )

    @functools.cached_property
    def __stance(self) -> int:
        return (
            self.__template.stance_base * self.__monster.stance_modify_ratio + self.__monster.stance_modify_value
        ) // 3

    def attr_changes_wiki(self) -> list[str]:
        from .monster import MonsterConfig

        attr_changes: list[str] = []
        for name, modify_ratio in (
            ("攻击", MonsterConfig.attack_modify_ratio),
            ("防御", MonsterConfig.defence_modify_ratio),
            ("生命", MonsterConfig.hp_modify_ratio),
        ):
            monster_modify_ratio = modify_ratio.__get__(self.__monster)
            proto_modify_ratio = modify_ratio.__get__(self.__proto)
            if monster_modify_ratio != proto_modify_ratio:
                change = monster_modify_ratio / proto_modify_ratio * 100
                attr_changes.append("{}:{}".format(name, f"{change:.02f}".rstrip("0").removesuffix(".")))
        level = self.__hard_level_group.level
        proto_speed = self.__proto.speed(level)
        if self.__speed != proto_speed:
            change = self.__speed / proto_speed * 100
            attr_changes.append("速度:{}".format(f"{change:.02f}".rstrip("0").removesuffix(".")))
        proto_stance = self.__proto.stance()
        if self.__stance != proto_stance:
            change = self.__stance / proto_stance * 100
            attr_changes.append("韧性:{}".format(f"{change:.02f}".rstrip("0").removesuffix(".")))
        return attr_changes

    __ELEMENTS = [
        Element.Physical,
        Element.Fire,
        Element.Ice,
        Element.Thunder,
        Element.Wind,
        Element.Quantum,
        Element.Imaginary,
    ]

    @functools.cached_property
    def __resist_changes(self) -> list[tuple[Element, float]]:
        resist_changes: list[tuple[Element, float]] = []
        monster_resistances = self.__monster.damage_type_resistance()
        proto_resistances = self.__proto.damage_type_resistance()
        for damage_type in self.__ELEMENTS:
            monster_resistance = monster_resistances.get(damage_type, 0)
            proto_resistance = proto_resistances.get(damage_type, 0)
            if monster_resistance != proto_resistance:
                resist_changes.append((damage_type, monster_resistance - proto_resistance))
        return resist_changes

    def resist_more_wiki(self) -> list[str]:
        return [
            "{}:{}".format(element, f"{change * 100:.02f}".rstrip("0").removesuffix("."))
            for element, change in self.__resist_changes
            if change > 0
        ]

    def resist_less_wiki(self) -> list[str]:
        return [
            "{}:{}".format(element, f"{-change * 100:.02f}".rstrip("0").removesuffix("."))
            for element, change in self.__resist_changes
            if change < 0
        ]

    def weakness_more_wiki(self) -> list[Element]:
        monster_weaknesses = set(self.__monster.weakness())
        proto_weaknesses = set(self.__proto.weakness())
        return [
            element for element in self.__ELEMENTS if element in monster_weaknesses and element not in proto_weaknesses
        ]

    def weakness_less_wiki(self) -> list[Element]:
        monster_weaknesses = set(self.__monster.weakness())
        proto_weaknesses = set(self.__proto.weakness())
        return [
            element for element in self.__ELEMENTS if element not in monster_weaknesses and element in proto_weaknesses
        ]

    def is_special(self) -> bool:
        return (
            len(self.attr_changes_wiki()) != 0
            or len(self.resist_less_wiki()) != 0
            or len(self.resist_more_wiki()) != 0
            or len(self.weakness_less_wiki()) != 0
            or len(self.weakness_more_wiki()) != 0
        )


class ChallengeGroupConfig(View[excel.ChallengeGroupConfig]):
    ExcelOutput: typing.Final = excel.ChallengeGroupConfig

    @property
    def id(self) -> int:
        return self._excel.id

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.group_name)

    @property
    def type(self) -> challenge.Type:
        return self._excel.challenge_group_type

    @property
    def issue(self) -> int:  # noqa: PLR0911
        """第几期，混沌回忆特殊一些"""
        match self._excel.challenge_group_type:
            case challenge.Type.Memory:
                match self._excel.id:
                    # 100 是常驻「永屹之城的遗秘」
                    # 900 是常驻「天艟求仙迷航录」
                    # 101 ~ 119 是开服前和开服后 1.x 版本的
                    case i if i in range(100, 110):
                        return 0
                    case 900:
                        return 0
                    case i if i in range(116, 120):
                        return self.id - 116
                    case i if i in range(110, 116):
                        return self.id - 106
                    case _:
                        # 1.3 迄今的混沌回忆
                        return self.id - 991
            case challenge.Type.Story:
                return self.id - 2000
            case challenge.Type.Boss:
                return self.id - 3000

    @functools.cached_property
    def __schedule(self) -> ScheduleData | None:
        if self._excel.schedule_data_id is None:
            return None
        match self._excel.challenge_group_type:
            case challenge.Type.Memory:
                method = self._game.schedule_data_challenge_maze
            case challenge.Type.Story:
                method = self._game.schedule_data_challenge_story
            case challenge.Type.Boss:
                method = self._game.schedule_data_challenge_boss
        schedule = method(self._excel.schedule_data_id)
        assert schedule is not None
        return schedule

    def schedule(self) -> ScheduleData | None:
        from .misc import ScheduleData

        return None if self.__schedule is None else ScheduleData(self._game, self.__schedule._excel)

    @functools.cached_property
    def __extra(self) -> ChallengeGroupExtra | ChallengeStoryGroupExtra | ChallengeBossGroupExtra:
        match self._excel.challenge_group_type:
            case challenge.Type.Memory:
                method = self._game.challenge_maze_group_extra
            case challenge.Type.Story:
                method = self._game.challenge_story_group_extra
            case challenge.Type.Boss:
                method = self._game.challenge_boss_group_extra
        extra = method(self._excel.id)
        assert extra is not None
        return extra

    def extra(self) -> ChallengeGroupExtra | ChallengeStoryGroupExtra | ChallengeBossGroupExtra:
        match self.__extra:
            case ChallengeGroupExtra():
                return ChallengeGroupExtra(self._game, self.__extra._excel)
            case ChallengeStoryGroupExtra():
                return ChallengeStoryGroupExtra(self._game, self.__extra._excel)
            case ChallengeBossGroupExtra():
                return ChallengeBossGroupExtra(self._game, self.__extra._excel)

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff | None:
        if self._excel.maze_buff_id is None:
            return None
        maze_buff = self._game.maze_buff(self._excel.maze_buff_id, 1)
        assert maze_buff is not None
        return maze_buff

    def maze_buff(self) -> MazeBuff | None:
        from .misc import MazeBuff

        return None if self.__maze_buff is None else MazeBuff(self._game, self.__maze_buff._excel)

    @functools.cached_property
    def __mazes(self) -> list[ChallengeMazeConfig]:
        mazes = self._game._challenge_group_mazes.get(self._excel.group_id)  # pyright: ignore[reportPrivateUsage]
        if mazes is None:
            return []
        return [ChallengeMazeConfig(self._game, maze) for maze in mazes]

    def mazes(self) -> collections.abc.Iterable[ChallengeMazeConfig]:
        return (ChallengeMazeConfig(self._game, maze._excel) for maze in self.__mazes)

    def __memory_wiki_special_monsters(self) -> dict[int, SpecialMonster]:
        special_monsters: dict[int, SpecialMonster] = {}
        for floor, maze in enumerate(self.__mazes):
            for event in (maze.event_1(), maze.event_2()):
                hard_level_group = event.hard_level_group()
                for wave in event.monster_lists():
                    for monster in wave:
                        if monster.id in special_monsters:
                            special_monsters[monster.id].append_floor(maze.floor or floor + 1)
                        else:
                            special_monsters[monster.id] = SpecialMonster(
                                monster, hard_level_group, maze.floor or floor + 1
                            )
        return special_monsters

    def __memory_wiki(self) -> str:
        if self.issue < 16:
            return f"{{{{混沌单期|期数={self.issue:03}|名称={self.name}}}}} <!-- 过早数据，不考虑兼容 -->"
        for maze in self.__mazes:
            assert len(list(maze.events_1())) == 1, "上半场景中无分立敌方首领"
            assert len(list(maze.events_2())) == 1, "下半场景中无分立敌方首领"
        return self._game._template_environment.get_template("混沌回忆单期3.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            challenge=self, special_monsters=self.__memory_wiki_special_monsters()
        )

    def __story_wiki_assertions(self):
        assert isinstance(self.__extra, ChallengeStoryGroupExtra)
        assert len(self.__extra._excel.buff_list) == 3, "虚构叙事固定三个战意机制"
        for maze in self.__mazes:
            events_1, events_2 = list(maze.events_1()), list(maze.events_2())
            assert len(events_1) == 1, "上半场景中无分立敌方首领"
            assert len(events_2) == 1, "下半场景中无分立敌方首领"
            stage_infinite_group_1 = events_1[0].stage_infinite_group()
            stage_infinite_group_2 = events_2[0].stage_infinite_group()
            assert stage_infinite_group_1 is not None
            assert stage_infinite_group_2 is not None
            for wave in stage_infinite_group_1.waves():
                group = list(wave.monster_groups())
                assert len(group) == 1, "上半每一波只有一个敌人组"
                for monster in group[0].monsters():
                    assert events_1[0]._excel.hard_level_group == monster._excel.hard_level_group, (
                        "monster 的 hard_level_group 和 stage 的 hard_level_group 应当是同一个"
                    )
            for wave in stage_infinite_group_2.waves():
                group = list(wave.monster_groups())
                assert len(group) == 1, "下半每一波只有一个敌人组"
                for monster in group[0].monsters():
                    assert events_2[0]._excel.hard_level_group == monster._excel.hard_level_group, (
                        "monster 的 hard_level_group 和 stage 的 hard_level_group 应当是同一个"
                    )

    def __story_wiki_special_monsters(self) -> dict[int, SpecialMonster]:
        special_monsters: dict[int, SpecialMonster] = {}
        for maze in self.__mazes:
            assert maze.floor is not None
            for event in (maze.event_1(), maze.event_2()):
                stage_infinite_group = event.stage_infinite_group()
                assert stage_infinite_group is not None
                hard_level_group = event.hard_level_group()
                for wave in stage_infinite_group.waves():
                    for monster in list(wave.monster_groups())[0].monsters():
                        if monster.id not in special_monsters:
                            special_monsters[monster.id] = SpecialMonster(monster, hard_level_group, maze.floor)
                        else:
                            special_monsters[monster.id].append_floor(maze.floor)
        return special_monsters

    def __story_wiki(self) -> str:
        if self.issue < 11:
            # TODO: 11 期之前的模板，实在是懒得写了，以后有空再说
            return f"{{{{虚构叙事单期|期数={self.issue:03}|名称={self.name}}}}} <!-- 过早数据，不考虑兼容 -->"
        self.__story_wiki_assertions()
        return self._game._template_environment.get_template("虚构叙事单期2.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            challenge=self, StoryType=challenge.StoryType, special_monsters=self.__story_wiki_special_monsters()
        )

    def __boss_wiki_assertions(self):
        prev_template_1: MonsterTemplateConfig | None = None
        prev_template_2: MonsterTemplateConfig | None = None
        for maze in self.__mazes:
            assert maze._excel.maze_buff_id == self.__mazes[0]._excel.maze_buff_id, "同期增益相同"
            # 上半
            events = list(maze.events_1())
            assert len(events) == 1, "上半场景中无分立敌方首领"
            waves = events[0].monster_lists()
            assert len(waves) == 1, "上半只有一波怪物"
            # 敌方可能会召唤随从，随从会出现在 monster_list 中，我们直接无视非首项
            # 目前唯一会召唤随从的特例：可可利亚会召唤杰帕德
            template = waves[0][0].template()
            assert template is not None, "逐光捡金中不会出现空模板敌方"
            if prev_template_1 is not None:
                assert template.id == prev_template_1.id, "上半同期怪物模板相同"
            prev_template_1 = template
            # 下半
            events = list(maze.events_2())
            assert len(events) == 1, "下半场景中无分立敌方首领"
            waves = events[0].monster_lists()
            assert len(waves) == 1, "下半只有一波怪物"
            template = waves[0][0].template()
            assert template is not None, "逐光捡金中不会出现空模板敌方"
            if prev_template_2 is not None:
                assert template.id == prev_template_2.id, "下半同期怪物模板相同"
            prev_template_2 = template
        # 终焉公理
        assert isinstance(self.__extra, ChallengeBossGroupExtra)
        assert len(self.__extra._excel.buff_list_1) == 3, "末日幻影固定 3 个增益"
        assert len(self.__extra._excel.buff_list_2) == 3, "末日幻影固定 3 个增益"

    def __boss_wiki(self) -> str:
        self.__boss_wiki_assertions()
        return self._game._template_environment.get_template("末日幻影单期.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            challenge=self,
        )

    def wiki(self):
        match self._excel.challenge_group_type:
            case challenge.Type.Memory:
                return self.__memory_wiki()
            case challenge.Type.Story:
                return self.__story_wiki()
            case challenge.Type.Boss:
                return self.__boss_wiki()


class ChallengeGroupExtra(View[excel.ChallengeGroupExtra]):
    ExcelOutput: typing.Final = excel.ChallengeGroupExtra


class ChallengeStoryGroupExtra(View[excel.ChallengeStoryGroupExtra]):
    ExcelOutput: typing.Final = excel.ChallengeStoryGroupExtra

    @property
    def type(self) -> challenge.StoryType:
        return self._excel.story_type

    @functools.cached_property
    def __sub_maze_buffs(self) -> list[MazeBuff] | None:
        assert self._excel.sub_maze_buff_list is not None, "虚构叙事固定存在战意机制"
        assert len(self._excel.sub_maze_buff_list) == 3, "虚构叙事固定 3 个战意机制"
        maze_buffs = [self._game.maze_buff(buff, 1) for buff in self._excel.sub_maze_buff_list]
        for buff in maze_buffs:
            assert buff is not None
        return typing.cast(list["MazeBuff"], maze_buffs)

    def sub_maze_buff(self) -> collections.abc.Iterable[MazeBuff] | None:
        from .misc import MazeBuff

        if self.__sub_maze_buffs is None:
            return None
        return (MazeBuff(self._game, buff._excel) for buff in self.__sub_maze_buffs)

    @functools.cached_property
    def __buffs(self) -> list[MazeBuff]:
        assert len(self._excel.buff_list) == 3, "虚构叙事固定 3 个荒腔走板"
        maze_buffs = [self._game.maze_buff(buff, 1) for buff in self._excel.buff_list]
        for buff in maze_buffs:
            assert buff is not None
        return typing.cast(list["MazeBuff"], maze_buffs)

    def buffs(self) -> collections.abc.Iterable[MazeBuff]:
        from .misc import MazeBuff

        return (MazeBuff(self._game, buff._excel) for buff in self.__buffs)


class ChallengeBossGroupExtra(View[excel.ChallengeBossGroupExtra]):
    ExcelOutput: typing.Final = excel.ChallengeBossGroupExtra

    @functools.cached_property
    def __buffs_1(self) -> list[MazeBuff]:
        buffs: list[MazeBuff] = []
        for buff_id in self._excel.buff_list_1:
            buff = self._game.maze_buff(buff_id, 1)
            assert buff is not None
            buffs.append(buff)
        return buffs

    def buffs_1(self) -> collections.abc.Iterable[MazeBuff]:
        from .misc import MazeBuff

        return (MazeBuff(self._game, buff._excel) for buff in self.__buffs_1)

    @functools.cached_property
    def __buffs_2(self) -> list[MazeBuff]:
        buffs: list[MazeBuff] = []
        for buff_id in self._excel.buff_list_2:
            buff = self._game.maze_buff(buff_id, 1)
            assert buff is not None
            buffs.append(buff)
        return buffs

    def buffs_2(self) -> collections.abc.Iterable[MazeBuff]:
        from .misc import MazeBuff

        return (MazeBuff(self._game, buff._excel) for buff in self.__buffs_2)


class ChallengeMazeConfig(View[excel.ChallengeMazeConfig]):
    ExcelOutput: typing.Final = excel.ChallengeMazeConfig

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @property
    def floor(self) -> int | None:
        return self._excel.floor

    @functools.cached_property
    def __group(self) -> ChallengeGroupConfig:
        group = (
            None
            or self._game.challenge_group_config(self._excel.group_id)
            or self._game.challenge_story_group_config(self._excel.group_id)
            or self._game.challenge_boss_group_config(self._excel.group_id)
        )
        assert group is not None
        return group

    def group(self) -> ChallengeGroupConfig:
        return ChallengeGroupConfig(self._game, self.__group._excel)

    @functools.cached_property
    def __extra(self) -> ChallengeStoryMazeExtra | ChallengeBossMazeExtra | None:
        match self.__group.type:
            case challenge.Type.Memory:
                return None
            case challenge.Type.Story:
                method = self._game.challenge_story_maze_extra
            case challenge.Type.Boss:
                method = self._game.challenge_boss_maze_extra
        extra = method(self._excel.id)
        assert extra is not None
        return None

    def extra(self) -> ChallengeStoryMazeExtra | ChallengeBossMazeExtra | None:
        if self.__extra is None:
            return None
        match self.__extra:
            case ChallengeStoryMazeExtra():
                return ChallengeStoryMazeExtra(self._game, self.__extra._excel)
            case ChallengeBossMazeExtra():
                return ChallengeBossMazeExtra(self._game, self.__extra._excel)

    def damage_type_1(self) -> list[Element]:
        return list(self._excel.damage_type_1)

    def damage_type_2(self) -> list[Element]:
        return list(self._excel.damage_type_2)

    @functools.cached_property
    def __events_1(self) -> list[StageConfig]:
        return list(self._game.stage_config(self._excel.event_id_list_1))

    def events_1(self) -> collections.abc.Iterable[StageConfig]:
        from .stage import StageConfig

        return (StageConfig(self._game, stage._excel) for stage in self.__events_1)

    def event_1(self) -> StageConfig:
        from .stage import StageConfig

        return StageConfig(self._game, self.__events_1[0]._excel)

    @functools.cached_property
    def __events_2(self) -> list[StageConfig]:
        return list(self._game.stage_config(self._excel.event_id_list_2))

    def events_2(self) -> collections.abc.Iterable[StageConfig]:
        from .stage import StageConfig

        return (StageConfig(self._game, stage._excel) for stage in self.__events_2)

    def event_2(self) -> StageConfig:
        from .stage import StageConfig

        return StageConfig(self._game, self.__events_2[0]._excel)

    @functools.cached_property
    def __maze_buff(self) -> MazeBuff:
        maze_buff = self._game.maze_buff(self._excel.maze_buff_id, 1)
        assert maze_buff is not None
        return maze_buff

    def maze_buff(self) -> MazeBuff:
        from .misc import MazeBuff

        return MazeBuff(self._game, self.__maze_buff._excel)


class ChallengeStoryMazeExtra(View[excel.ChallengeStoryMazeExtra]):
    ExcelOutput: typing.Final = excel.ChallengeStoryMazeExtra


class ChallengeBossMazeExtra(View[excel.ChallengeBossMazeExtra]):
    ExcelOutput: typing.Final = excel.ChallengeBossMazeExtra


class ChallengeTargetConfig(View[excel.ChallengeTargetConfig]):
    ExcelOutput: typing.Final = excel.ChallengeTargetConfig


class RewardLine(View[excel.RewardLine]):
    ExcelOutput: typing.Final = excel.RewardLine
