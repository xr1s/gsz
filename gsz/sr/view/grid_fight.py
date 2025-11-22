from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from ..excel.grid_fight import FrontBackType, Quality
    from .avatar import AvatarConfig, AvatarSkillConfig


class GridFightAugment(View[excel.GridFightAugment]):
    ExcelOutput: typing.Final = excel.GridFightAugment

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.hex_name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.hex_desc)

    @property
    def desc_params(self) -> tuple[float, ...]:
        return tuple(desc.value for desc in self._excel.desc_param_list)

    @property
    def quality(self) -> Quality:
        return self._excel.quality


class GridFightBackRoleRank(View[excel.GridFightBackRoleRank]):
    ExcelOutput: typing.Final = excel.GridFightBackRoleRank

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc)

    @property
    def desc_params(self) -> tuple[float, ...]:
        return self._excel.desc_param_list


class GridFightFrontSkill(View[excel.GridFightFrontSkill]):
    ExcelOutput: typing.Final = excel.GridFightFrontSkill

    @functools.cached_property
    def name(self) -> str | None:
        return self._game.text(self._excel.skill_name) if self._excel.skill_name is not None else None

    @functools.cached_property
    def desc(self) -> str | None:
        return self._game.text(self._excel.skill_desc) if self._excel.skill_desc is not None else None

    @property
    def params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.param_list)


class GridFightRoleBasicInfo(View[excel.GridFightRoleBasicInfo]):
    ExcelOutput: typing.Final = excel.GridFightRoleBasicInfo

    @property
    def id(self) -> int:
        return self._excel.id_

    @property
    def name(self) -> str:
        return self.__avatar.name

    @property
    def rarity(self) -> typing.Literal[1, 2, 3, 4, 5]:
        return self._excel.rarity

    @property
    def front_back_type(self) -> FrontBackType | None:
        return self._excel.front_back_type

    @functools.cached_property
    def __avatar(self) -> AvatarConfig:
        avatar = self._game.avatar_config(self._excel.avatar_id)
        if avatar is None:
            avatar = self._game.avatar_config_ld(self._excel.avatar_id)
            assert avatar is not None
        return avatar

    def avatar(self) -> AvatarConfig:
        from .avatar import AvatarConfig

        return AvatarConfig(self._game, self.__avatar._excel)

    @functools.cached_property
    def __skill_display(self) -> tuple[GridFightRoleSkillDisplay, ...]:
        return tuple(self._game.grid_fight_role_skill_display(self._excel.id_))

    @functools.cached_property
    def tags(self) -> tuple[str, ...]:
        tags: set[str] = set[str]()
        for skill_display in self.__skill_display:
            for tag_name in skill_display._excel.category_tag_list:
                tag = self._game.grid_fight_role_tag_info(tag_name)
                assert tag is not None
                tags.add(tag.desc)
        return tuple(tags)

    @functools.cached_property
    def __traits(self) -> tuple[GridFightTraitBasicInfo, ...]:
        return tuple(self._game.grid_fight_trait_basic_info(self._excel.trait_list))

    def traits(self) -> collections.abc.Iterable[GridFightTraitBasicInfo]:
        return (GridFightTraitBasicInfo(self._game, trait._excel) for trait in self.__traits)

    @functools.cached_property
    def __backend_ranks(self) -> tuple[GridFightBackRoleRank, ...]:
        return tuple(self._game.grid_fight_back_role_rank(self._excel.backend_rank_list))

    def backend_roles(self) -> collections.abc.Iterable[GridFightBackRoleRank]:
        return (GridFightBackRoleRank(self._game, trait._excel) for trait in self.__backend_ranks)


class GridFightRoleSkillDisplay(View[excel.GridFightRoleSkillDisplay]):
    ExcelOutput: typing.Final = excel.GridFightRoleSkillDisplay

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)


class GridFightRoleStar(View[excel.GridFightRoleStar]):
    ExcelOutput: typing.Final = excel.GridFightRoleStar

    @property
    def star(self) -> int:
        return self._excel.star

    @functools.cached_property
    def __skill_overrides(self) -> list[tuple[AvatarSkillConfig | None, GridFightFrontSkill]]:
        skill_pairs: list[tuple[AvatarSkillConfig | None, GridFightFrontSkill]] = []
        for src_id, dst_id in zip(self._excel.skill_override_src, self._excel.skill_override_dest, strict=True):
            src_skill = None
            if src_id != 0:
                src_skill = self._game.avatar_skill_config(src_id, 1) or self._game.avatar_skill_config_ld(src_id, 1)
                assert src_skill is not None
            dst_skill = self._game.grid_fight_front_skill(dst_id, 1)
            assert dst_skill is not None
            skill_pairs.append((src_skill, dst_skill))
        return skill_pairs

    def skill_overrides(self) -> collections.abc.Iterable[tuple[AvatarSkillConfig | None, GridFightFrontSkill]]:
        from .avatar import AvatarSkillConfig

        return (
            (
                AvatarSkillConfig(self._game, src._excel) if src is not None else None,
                GridFightFrontSkill(self._game, dst._excel),
            )
            for src, dst in self.__skill_overrides
        )


class GridFightRoleTagInfo(View[excel.GridFightRoleTagInfo]):
    ExcelOutput: typing.Final = excel.GridFightRoleTagInfo

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.tag_desc)


class GridFightTraitBasicInfo(View[excel.GridFightTraitBasicInfo]):
    ExcelOutput: typing.Final = excel.GridFightTraitBasicInfo

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.trait_name)

    @functools.cached_property
    def base_desc(self) -> str:
        return self._game.text(self._excel.trait_base_desc)

    @property
    def base_desc_params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.base_desc_param_list)
