from __future__ import annotations

import functools
import typing

from .. import excel
from ..excel import monster, stage
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .monster import EliteGroup, HardLevelGroup, MonsterConfig


class StageConfig(View[excel.StageConfig]):
    ExcelOutput: typing.Final = excel.StageConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.stage_name)

    @functools.cached_property
    def wave(self) -> int | None:
        return next((int(data.val) for data in self._excel.stage_config_data if data.key == stage.DataKey.Wave), None)

    @functools.cached_property
    def __monster_lists(self) -> list[list[MonsterConfig]]:
        monster_lists: list[list[MonsterConfig]] = []
        for monster_list in self._excel.monster_list:
            wave = monster_list
            if len(monster_list) == 3:
                wave = [monster_list[1], monster_list[2], monster_list[0]]
            elif len(monster_list) == 4:
                wave = [monster_list[2], monster_list[3], monster_list[0], monster_list[1]]
            monster_lists.append(list(self._game.monster_config(wave)))
        return monster_lists

    def monster_lists(self) -> list[list[MonsterConfig]]:
        from .monster import MonsterConfig

        return [
            [MonsterConfig(self._game, monster._excel) for monster in [*monster_list[1:], monster_list[0]]]
            for monster_list in self.__monster_lists
        ]

    @functools.cached_property
    def __stage_infinite_group(self) -> StageInfiniteGroup | None:
        stage_infinite_group_id = next(
            (int(data.val) for data in self._excel.stage_config_data if data.key == stage.DataKey.StageInfiniteGroup),
            None,
        )
        if stage_infinite_group_id in (None, 30023012):  # 缺数据
            return None
        stage_infinite_group = self._game.stage_infinite_group(stage_infinite_group_id)
        assert stage_infinite_group is not None
        return stage_infinite_group

    def stage_infinite_group(self) -> StageInfiniteGroup | None:
        return (
            None
            if self.__stage_infinite_group is None
            else StageInfiniteGroup(self._game, self.__stage_infinite_group._excel)
        )

    @functools.cached_property
    def __hard_level_group(self) -> HardLevelGroup:
        hard_level_group = self._game.hard_level_group(self._excel.hard_level_group, self._excel.level)
        assert hard_level_group is not None
        return hard_level_group

    def hard_level_group(self) -> HardLevelGroup:
        from .monster import HardLevelGroup

        return HardLevelGroup(self._game, self.__hard_level_group._excel)


class StageInfiniteGroup(View[excel.StageInfiniteGroup]):
    ExcelOutput: typing.Final = excel.StageInfiniteGroup

    @functools.cached_property
    def __waves(self) -> list[StageInfiniteWaveConfig]:
        return list(self._game.stage_infinite_wave_config(self._excel.wave_id_list))

    def waves(self) -> collections.abc.Iterable[StageInfiniteWaveConfig]:
        return (StageInfiniteWaveConfig(self._game, wave._excel) for wave in self.__waves)

    def max_teammate_count(self) -> list[int]:
        max_teammate_count = [wave.max_teammate_count for wave in self.__waves]
        if max_teammate_count[0] == max_teammate_count[1] == max_teammate_count[2]:
            return [max_teammate_count[0]]
        return max_teammate_count


class StageInfiniteMonsterGroup(View[excel.StageInfiniteMonsterGroup]):
    ExcelOutput: typing.Final = excel.StageInfiniteMonsterGroup

    @functools.cached_property
    def __elite_group(self) -> EliteGroup | None:
        if self._excel.elite_group is None:
            return None
        elite_group = self._game.elite_group(self._excel.elite_group)
        assert elite_group is not None
        return elite_group

    def elite_group(self) -> EliteGroup | None:
        from .monster import EliteGroup

        return None if self.__elite_group is None else EliteGroup(self._game, self.__elite_group._excel)

    @functools.cached_property
    def __monsters(self) -> list[MonsterConfig]:
        return list(
            self._game.monster_config(
                filter(lambda monster_id: monster_id not in (0, 300205001), self._excel.monster_list)
            )
        )

    def monsters(self) -> collections.abc.Iterable[MonsterConfig]:
        from .monster import MonsterConfig

        return (MonsterConfig(self._game, monster._excel) for monster in self.__monsters)


class StageInfiniteWaveConfig(View[excel.StageInfiniteWaveConfig]):
    ExcelOutput: typing.Final = excel.StageInfiniteWaveConfig

    @property
    def max_teammate_count(self) -> int:
        """每一波次场上最多多少敌人"""
        return self._excel.max_teammate_count

    @functools.cached_property
    def __monster_groups(self) -> list[StageInfiniteMonsterGroup]:
        return list(self._game.stage_infinite_monster_group(self._excel.monster_group_id_list))

    def monster_groups(self) -> collections.abc.Iterable[StageInfiniteMonsterGroup]:
        return (StageInfiniteMonsterGroup(self._game, monster_group._excel) for monster_group in self.__monster_groups)

    def story_wiki_aggregate(self) -> str:
        monster_names: dict[str, int] = {}
        for group in self.__monster_groups:
            for enemy in group.monsters():
                if enemy.rank not in (monster.Rank.Minion, monster.Rank.MinionLv2):
                    continue
                if enemy.wiki_name not in monster_names:
                    monster_names[enemy.wiki_name] = 1
                else:
                    monster_names[enemy.wiki_name] += 1
        return "、".join(f"{name}:{count}" for name, count in monster_names.items())

    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)

    def story_wiki_elite(self) -> str:
        monster_names: dict[str, int] = {}
        for group in self.__monster_groups:
            for enemy in group.monsters():
                if enemy.rank in (monster.Rank.Minion, monster.Rank.MinionLv2):
                    continue
                if enemy.wiki_name not in monster_names:
                    monster_names[enemy.wiki_name] = 1
                else:
                    monster_names[enemy.wiki_name] += 1
        return "、".join(f"{name}:{count}" for name, count in monster_names.items())

    @functools.cached_property
    def __elite_groups(self) -> list[EliteGroup]:
        return list(filter(None, (group.elite_group() for group in self.__monster_groups)))

    def elite_groups(self) -> collections.abc.Iterable[EliteGroup]:
        from .monster import EliteGroup

        return (EliteGroup(self._game, group._excel) for group in self.__elite_groups)
