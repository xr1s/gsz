import functools

from .. import excel
from .base import View


class EliteGroup(View[excel.EliteGroup]):
    """精英组别，属性加成"""

    ExcelOutput: type = excel.EliteGroup


class HardLevelGroup(View[excel.HardLevelGroup]):
    """敌方属性成长详情"""

    ExcelOutput: type = excel.HardLevelGroup


NPC_COLLIDE_NAMES = {"可可利亚", "杰帕德", "布洛妮娅", "史瓦罗", "银枝"}


class MonsterConfig(View[excel.MonsterConfig]):
    """怪物详情"""

    ExcelOutput: type = excel.MonsterConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.monster_name)

    @functools.cached_property
    def wiki_name(self) -> str:
        # 和 NPC 或者自机角色同名的敌方
        # 「（完整）」版本不需要额外加「（敌方）」
        if self.name in NPC_COLLIDE_NAMES:
            return self.name + "（敌方）"
        name = self.name
        # 不知为何 WIKI 上自动机兵都使用「•」做分隔符而非保留原来的
        if self.name.startswith("自动机兵「"):
            end = name.find("」", 5)
            suffix = name[end + 1 :]  # 可能是「（完整）」、「（错误）」等后缀
            name = f"自动机兵•{name[5:end]}{suffix}"
        # 仅出现在「入魔机巧」系列魔物中
        if name.find("\xa0") != -1:
            name = name.replace("\xa0", "")
        # WIKI 中大量使用「、」作为分隔符，因此当怪物名称中出现「、」时需要额外转义
        # 仅出现在「昔在、今在、永在的剧目」系列魔物中
        if name.find("、") != -1:
            name = name.replace("、", "&#x3001;")
        return name
