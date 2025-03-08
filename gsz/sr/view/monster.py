from __future__ import annotations
import functools
import itertools
from typing import TYPE_CHECKING

from .. import excel
from ...format import Formatter
from .base import View

if TYPE_CHECKING:
    from ..excel import Element


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
    if name.find("\xa0") != -1:
        name = name.replace("\xa0", "")
    # WIKI 中大量使用「、」作为分隔符，因此当敌人名称中出现「、」时需要额外转义
    # 仅出现在「昔在、今在、永在的剧目」系列敌人中
    if name.find("、") != -1:
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


NPC_COLLIDE_NAMES = {"可可利亚", "杰帕德", "布洛妮娅", "史瓦罗", "银枝"}


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
        hard_level_group = self._game.hard_level_group(self._excel.hard_level_group, level - 1)
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
        hard_level_group = self._game.hard_level_group(self._excel.hard_level_group, level - 1)
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


class MonsterSkillConfig(View[excel.MonsterSkillConfig]):
    type ExcelOutput = excel.MonsterSkillConfig

    @staticmethod
    @functools.cache
    def __formatter():
        return Formatter()

    @functools.cached_property
    def name(self) -> str:
        # 此处格式化是为了去除 <unbreak>
        return self.__formatter().format(self._game.text(self._excel.skill_name))

    @property
    def damage_type(self) -> Element | None:
        """伤害属性，无伤害则 None"""
        return self._excel.damage_type

    @property
    def phase_list(self) -> list[int]:
        """敌人的哪几个阶段会有本技能"""
        return self._excel.phase_list

    @functools.cached_property
    def param_list(self) -> list[float]:
        return [param.value for param in self._excel.param_list]

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
