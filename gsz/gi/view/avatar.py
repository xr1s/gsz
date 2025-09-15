from __future__ import annotations

import functools
import typing

from .. import excel
from ..excel import Element, avatar
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc


class Avatar(View[excel.Avatar]):
    ExcelBinOutput: typing.Final = excel.Avatar

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name_text_map_hash)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc_text_map_hash)

    @property
    def body_type(self) -> avatar.BodyType:
        return self._excel.body_type

    @property
    def rarity(self) -> typing.Literal[4, 5]:
        return 4 if self._excel.quality_type is avatar.QualityType.Purple else 5

    @property
    def weapon_type(self) -> avatar.WeaponType:
        return self._excel.weapon_type

    @property
    def is_playable(self) -> bool:
        return self._excel.use_type is avatar.UseType.Formal and not self.name.endswith("(试用)")

    @functools.cached_property
    def element(self) -> Element | None:  # 目前看只有主角是 None
        skill = self.__skill_depot.energy_skill()
        if skill is None:
            return None
        if skill._excel.cost_elem_type == "None":
            return None
        return skill._excel.cost_elem_type

    @functools.cached_property
    def __skill_depot(self) -> AvatarSkillDepot:
        skill_depot = self._game.avatar_skill_depot(self._excel.skill_depot_id)
        assert skill_depot is not None
        return skill_depot

    def skill_depot(self) -> AvatarSkillDepot:
        return self.__skill_depot


class AvatarSkill(View[excel.AvatarSkill]):
    ExcelBinOutput: typing.Final = excel.AvatarSkill

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name_text_map_hash)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc_text_map_hash)


class AvatarSkillDepot(View[excel.AvatarSkillDepot]):
    ExcelBinOutput: typing.Final = excel.AvatarSkillDepot

    @functools.cached_property
    def __skills(self) -> tuple[AvatarSkill, ...]:
        return tuple(self._game.avatar_skill(filter(None, self._excel.skills)))

    def skills(self) -> collections.abc.Iterable[AvatarSkill]:
        return (AvatarSkill(self._game, skill._excel) for skill in self.__skills)

    @functools.cached_property
    def __energy_skill(self) -> AvatarSkill | None:  # 只有测试数据和主角是 None
        return self._game.avatar_skill(self._excel.energy_skill)

    def energy_skill(self) -> AvatarSkill | None:  # 只有测试数据和主角是 None
        return AvatarSkill(self._game, self.__energy_skill._excel) if self.__energy_skill is not None else None
