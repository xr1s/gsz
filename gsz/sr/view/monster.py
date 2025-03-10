from __future__ import annotations
import functools
import itertools
import re
from typing import TYPE_CHECKING

from .. import excel
from .base import View

if TYPE_CHECKING:
    import collections.abc
    from ..excel import Element, monster

NPC_COLLIDE_NAMES = {"可可利亚", "杰帕德", "布洛妮娅", "史瓦罗", "银枝"}


def wiki_name(name: str) -> str:
    # 和 NPC 或者自机角色同名的敌方
    # 「（完整）」版本不需要额外加「（敌方）」
    if name in NPC_COLLIDE_NAMES:
        return name + "（敌方）"
    # 不知为何 WIKI 上自动机兵都使用「•」做分隔符而非保留原来的
    if name.startswith("自动机兵「"):
        end = name.find("」", 5)
        suffix = name[end + 1 :]  # 可能是「（完整）」、「（错误）」等后缀
        name = f"自动机兵•{name[5:end]}{suffix}"
    # 仅出现在「入魔机巧」系列魔物中
    if "\xa0" in name:
        name = name.replace("\xa0", "")
    # WIKI 中大量使用「、」作为分隔符，因此当敌人名称中出现「、」时需要额外转义
    # 仅出现在「昔在、今在、永在的剧目」系列敌人中
    if "、" in name:
        name = name.replace("、", "&#x3001;")
    return name


class EliteGroup(View[excel.EliteGroup]):
    """精英组别，属性加成"""

    type ExcelOutput = excel.EliteGroup


class HardLevelGroup(View[excel.HardLevelGroup]):
    """敌方属性成长详情"""

    type ExcelOutput = excel.HardLevelGroup

    @property
    def hp_ratio(self) -> float:
        return self._excel.hp_ratio.value

    @property
    def speed_ratio(self) -> float:
        return self._excel.speed_ratio.value


class MonsterCamp(View[excel.MonsterCamp]):
    """敌人阵营"""

    type ExcelOutput = excel.MonsterCamp

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class MonsterConfig(View[excel.MonsterConfig]):
    """
    敌人详情

    对应游戏中的每种敌人
    和 Template 的差别是会随着环境修改具体的属性数值
    比如在深渊里的会适当调高降低属性等
    """

    type ExcelOutput = excel.MonsterConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.monster_name)

    @functools.cached_property
    def wiki_name(self) -> str:
        return wiki_name(self.name)

    @functools.cached_property
    def template(self) -> MonsterTemplateConfig | None:
        template = self._game.monster_template_config(self._excel.monster_template_id)
        if template is None:
            template = self._game.monster_template_unique_config(self._excel.monster_template_id)
        return template  # 注意 1.0~1.3, 2.0 存在几个数据会返回 None

    def hp(self, level: int | None = None) -> float:
        """
        敌人在 level 等级时的生命值上限
        未传入 level 时返回基础生命值

        需要注意基础生命值未必等于 1 级的生命值
        """
        if self.template is None:
            return 0.0
        if level is None:
            return self.template.hp_base * self._excel.hp_modify_ratio.value
        hard_level_group = self._game.hard_level_group(self._excel.hard_level_group, level)
        if hard_level_group is None:
            return 0.0
        return self.template.hp_base * self._excel.hp_modify_ratio.value * hard_level_group.hp_ratio

    def speed(self, level: int | None = None) -> float:
        """
        敌人在 level 等级时的速度
        未传入 level 时返回基础速度

        需要注意基础速度未必等于 1 级的速度
        """
        if self.template is None:
            return 0.0
        monster_speed_base = (
            self.template.speed_base * self._excel.speed_modify_ratio.value + self._excel.speed_modify_value.value
        )
        if level is None:
            return monster_speed_base
        hard_level_group = self._game.hard_level_group(self._excel.hard_level_group, level)
        if hard_level_group is None:
            return 0.0
        return monster_speed_base * hard_level_group.speed_ratio

    def stance(self) -> int:
        """敌方韧性，不随等级变化"""
        if self.template is None:
            return 0
        # 我也不知道为什么这个要除以三，但游戏里是这样的
        return (
            self.template.stance_base * self._excel.stance_modify_ratio.value + self._excel.stance_modify_value.value
        ) // 3

    @functools.cached_property
    def introduction(self) -> str:
        return self._game.text(self._excel.monster_introduction) if self._excel.monster_introduction is not None else ""

    @functools.cached_property
    def skills(self) -> list[MonsterSkillConfig]:
        return list(self._game.monster_skill_config(self._excel.skill_list))

    @functools.cached_property
    def damage_types(self) -> list[Element]:
        """所有可能的伤害属性，有些敌人可能不同技能有不同的伤害属性"""
        return list({skill.damage_type for skill in self.skills if skill.damage_type is not None})

    @functools.cached_property
    def phase(self) -> int:
        """敌人总共有多少阶段，只能从技能里找最大的那个 phase"""
        return max(itertools.chain.from_iterable(skill.phase_list for skill in self.skills), default=1)

    @functools.cached_property
    def summons(self) -> list[MonsterConfig]:
        """召唤物，不过这大概不完整，目前没找到能完整列出召唤物的手段"""
        summons: set[str] = set()
        return [
            summons.add(summon.name) or summon
            for summon in (self._game.monster_config(custom_value.val) for custom_value in self._excel.custom_values)
            if summon is not None and summon.name not in summons
        ]

    @property
    def weakness(self) -> list[Element]:
        return self._excel.stance_weak_list

    @property
    def rank(self) -> monster.Rank | None:
        if self.template is None:
            return None
        return self.template.rank

    @staticmethod
    def __element_resistance_name(element: Element) -> str:
        if element == element.Physical:
            return "物"
        return str(element)

    def skills_at_phase(self, phase: int) -> collections.abc.Iterable[MonsterSkillConfig]:
        """在 phase 阶段的技能列表，phase 从 1 开始计数"""
        return (skill for skill in self.skills if phase in skill.phase_list)

    def threat_count_at_phase(self, phase: int) -> int:
        """在 phase 阶段的大招数，phase 从 1 开始计数"""
        return sum(skill.is_threat for skill in self.skills_at_phase(phase))

    def wiki(self) -> str:
        damage_type_resistance = {
            MonsterConfig.__element_resistance_name(resistance.damage_type): f"{round(resistance.value.value * 100)}%"
            for resistance in self._excel.damage_type_resistance
        }
        element_resistance = [
            f"{resistance.damage_type}属性抗性"
            for resistance in self._excel.damage_type_resistance
            if resistance.value.value > 0.2
        ]
        debuff_resistance = [debuff.key for debuff in self._excel.debuff_resist]
        tags: list[str] = []
        if len(self.summons) != 0:
            tags.append("召唤")
        if self.name.endswith("（错误）"):
            tags.append("错误")
        if self.name.endswith("（完整）"):
            tags.append("完整")
        return self._game._template_environment.get_template("enemy.jinja2").render(  # pyright: ignore[reportPrivateUsage]
            monster=self,
            damage_type_resistance=damage_type_resistance,
            element_resistance=element_resistance,
            debuff_resistance=debuff_resistance,
            tags=tags,
        )


class MonsterSkillConfig(View[excel.MonsterSkillConfig]):
    type ExcelOutput = excel.MonsterSkillConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.skill_name)

    @property
    def damage_type(self) -> Element | None:
        """伤害属性，无伤害则 None"""
        return self._excel.damage_type

    @property
    def phase_list(self) -> list[int]:
        """敌人的哪几个阶段会有本技能"""
        return self._excel.phase_list

    @property
    def is_threat(self) -> bool:
        return self._excel.is_threat

    @property
    def sp_hit_base(self) -> int | None:
        if self._excel.sp_hit_base is None:
            return None
        return self._excel.sp_hit_base.value

    @functools.cached_property
    def tag(self) -> str:
        return self._game.text(self._excel.skill_tag)

    @functools.cached_property
    def param_list(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.skill_desc)


class MonsterTemplateConfig(View[excel.MonsterTemplateConfig]):
    type ExcelOutput = excel.MonsterTemplateConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.monster_name)

    @functools.cached_property
    def wiki_name(self) -> str:
        return wiki_name(self.name)

    @property
    def hp_base(self) -> float:
        return self._excel.hp_base.value

    @property
    def speed_base(self) -> float:
        return 0.0 if self._excel.speed_base is None else self._excel.speed_base.value

    @property
    def stance_base(self) -> int:
        return 0 if self._excel.stance_base is None else self._excel.stance_base.value

    @property
    def group_id(self) -> int | None:
        return self._excel.template_group_id

    @property
    def group(self) -> list[MonsterTemplateConfig]:
        if self.group_id is None:
            return [self]
        group = self._game._monster_template_group.get(self.group_id)  # pyright: ignore[reportPrivateUsage]
        if group is None:
            return [self]
        return [MonsterTemplateConfig(self._game, excel) for excel in group]

    @property
    def rank(self) -> monster.Rank:
        return self._excel.rank

    @functools.cached_property
    def wiki_rank(self) -> str:  # noqa: PLR0911
        """无法判断是否为末日幻影首领，需要填写的时候注意"""
        match self._excel.rank:
            case self._excel.rank.BigBoss:
                return "周本Boss"
            case self._excel.rank.Elite:
                if self.name.endswith("（错误）"):
                    return "模拟宇宙精英"
                return "强敌"
            case self._excel.rank.LittleBoss:
                if self.name.endswith("（完整）"):
                    return "模拟宇宙首领"
                return "剧情Boss"
            case self._excel.rank.Minion | self._excel.rank.MinionLv2:
                if self._excel.template_group_id is None:
                    return "召唤物"
                return "普通"

    @functools.cached_property
    def camp(self) -> MonsterCamp | None:
        if self._excel.monster_camp_id is None:
            return None
        return self._game.monster_camp(self._excel.monster_camp_id)

    # fmt: off
    MISSING_NPC_MONSTER: set[int] = {
        1005010, 1012010, 3024012, 8022020,
        2013011, # 1.2 缺漏数据
        4012050, # 3.0 缺漏数据
    }
    # fmt: on

    @functools.cached_property
    def npc_monster(self) -> list[NPCMonsterData]:
        return list(
            self._game.npc_monster_data(
                filter(lambda id: id not in self.MISSING_NPC_MONSTER, self._excel.npc_monster_list)
            )
        )


class NPCMonsterData(View[excel.NPCMonsterData]):
    type ExcelOutput = excel.NPCMonsterData

    @functools.cached_property
    def name(self) -> str:
        if self._excel.npc_name is None:
            return ""
        return self._game.text(self._excel.npc_name)
