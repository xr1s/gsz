from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from ..excel import fate
    from .avatar import AvatarConfig
    from .misc import MazeBuff


class FateBuff(View[excel.FateBuff]):
    ExcelOutput: typing.Final = excel.FateBuff

    @property
    def name(self) -> str:
        assert all(buff.name == self.__maze_buff[0].name for buff in self.__maze_buff)
        return self.__maze_buff[0].name

    @property
    def icon(self) -> str:
        return self._excel.icon

    @property
    def rarity(self) -> fate.BuffRarity:
        return self._excel.rarity

    @property
    def class_trait_id(self) -> int:
        return self._excel.class_trait_id

    @functools.cached_property
    def __class_trait(self) -> FateTrait:
        trait = self._game.fate_trait(self._excel.class_trait_id)
        assert trait is not None
        return trait

    @property
    def skill_trait_id(self) -> int:
        return self._excel.skill_trait_id

    @functools.cached_property
    def __skill_trait(self) -> FateTrait:
        trait = self._game.fate_trait(self._excel.skill_trait_id)
        assert trait is not None
        return trait

    def traits(self) -> tuple[FateTrait, FateTrait]:
        return (self.__class_trait, self.__skill_trait)

    @functools.cached_property
    def __maze_buff(self) -> tuple[MazeBuff, ...]:
        return tuple(self._game.fate_maze_buff(self._excel.maze_buff))

    def maze_buff(self) -> collections.abc.Iterable[MazeBuff]:
        from .misc import MazeBuff

        return (MazeBuff(self._game, maze_buff._excel) for maze_buff in self.__maze_buff)


class FateHandbookMaster(View[excel.FateHandbookMaster]):
    ExcelOutput: typing.Final = excel.FateHandbookMaster

    @property
    def strength(self) -> fate.Ability:
        """筋力"""
        return self._excel.strength

    @property
    def magical_energy(self) -> fate.Ability:
        """魔力"""
        return self._excel.magical_energy

    @property
    def endurance(self) -> fate.Ability:
        """耐久"""
        return self._excel.endurance

    @property
    def luck(self) -> fate.Ability:
        """幸运"""
        return self._excel.luck

    @property
    def agility(self) -> fate.Ability:
        """敏捷"""
        return self._excel.agility

    @property
    def noble_phantasm(self) -> fate.Ability:
        """宝具"""
        return self._excel.noble_phantasm

    @functools.cached_property
    def hougu_name(self) -> str:
        return self._game.text(self._excel.hougu_name)

    @functools.cached_property
    def skill_comment(self) -> str:
        return self._game.text(self._excel.skill_comment)

    @functools.cached_property
    def story(self) -> str:
        return self._game.text(self._excel.story)

    @functools.cached_property
    def wish(self) -> str:
        return self._game.text(self._excel.wish)


class FateMaster(View[excel.FateMaster]):
    ExcelOutput: typing.Final = excel.FateMaster

    @functools.cached_property
    def __avatar(self) -> AvatarConfig:
        avatar = self._game.avatar_config(self._excel.id_)
        assert avatar is not None
        return avatar

    def avatar(self) -> AvatarConfig:
        from .avatar import AvatarConfig

        return AvatarConfig(self._game, self.__avatar._excel)

    @functools.cached_property
    def __handbook(self) -> FateHandbookMaster:
        handbook = self._game.fate_handbook_master(self._excel.id_)
        assert handbook is not None
        return handbook

    def handbook(self) -> FateHandbookMaster:
        return FateHandbookMaster(self._game, self.__handbook._excel)

    @property
    def name(self) -> str:
        return self.__avatar.name

    @property
    def class_(self) -> str:
        return self._excel.class_.value

    @functools.cached_property
    def skill_name(self) -> str:
        return self._game.text(self._excel.skill_name)

    @functools.cached_property
    def skill_desc(self) -> str:
        return self._game.text(self._excel.skill_desc)

    @property
    def skill_param(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.skill_param)


class FateMasterTalk(View[excel.FateMasterTalk]):
    ExcelOutput: typing.Final = excel.FateMasterTalk

    @property
    def when(self) -> fate.TalkWhen:
        return self._excel.when

    @functools.cached_property
    def __this_avatar(self) -> AvatarConfig:
        avatar = self._game.avatar_config(self._excel.this_avatar_id)
        assert avatar is not None
        return avatar

    def this_avatar(self) -> AvatarConfig:
        from .avatar import AvatarConfig

        return AvatarConfig(self._game, self.__this_avatar._excel)

    @functools.cached_property
    def this_talk(self) -> str:
        return self._game.text(self._excel.this_avatar_talk)

    @functools.cached_property
    def __that_avatar(self) -> AvatarConfig | None:
        if self._excel.that_avatar_id is None:
            return None
        avatar = self._game.avatar_config(self._excel.that_avatar_id)
        assert avatar is not None
        return avatar

    def that_avatar(self) -> AvatarConfig | None:
        from .avatar import AvatarConfig

        return AvatarConfig(self._game, self.__that_avatar._excel) if self.__that_avatar is not None else None

    @functools.cached_property
    def that_talk(self) -> str:
        return self._game.text(self._excel.that_avatar_talk) if self._excel.that_avatar_talk is not None else ""


class FateReiju(View[excel.FateReiju]):
    ExcelOutput: typing.Final = excel.FateReiju

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @property
    def days(self) -> tuple[int, ...]:
        return tuple(self._excel.days)

    @property
    def corruption(self) -> int | None:
        return self._excel.corruption

    @property
    def category(self) -> fate.ReijuCategory:
        return self._excel.category

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc)

    @functools.cached_property
    def desc_simple(self) -> str:
        return self._game.text(self._excel.desc_simple)

    @functools.cached_property
    def params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.params)


class FateTrait(View[excel.FateTrait]):
    ExcelOutput: typing.Final = excel.FateTrait

    @property
    def id(self) -> int:
        return self._excel.id_

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc)

    @functools.cached_property
    def params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.params)

    @functools.cached_property
    def tag_1(self) -> str:
        return self._game.text(self._excel.tag_1)

    @functools.cached_property
    def tag_2(self) -> str | None:
        return self._game.text(self._excel.tag_2) if self._excel.tag_2 is not None else None

    @property
    def type(self) -> fate.TraitType:
        return self._excel.type_


class FateTraitBuff(View[excel.FateTraitBuff]):
    ExcelOutput: typing.Final = excel.FateTraitBuff

    @property
    def trait_id(self) -> int:
        return self._excel.trait_id

    @property
    def require(self) -> int:
        return self._excel.require

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.desc)

    @functools.cached_property
    def params(self) -> tuple[float, ...]:
        return tuple(param.value for param in self._excel.params)
