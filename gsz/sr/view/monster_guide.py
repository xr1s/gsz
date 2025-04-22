from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View

if typing.TYPE_CHECKING:
    import collections.abc

    from .misc import ExtraEffectConfig
    from .monster import MonsterSkillConfig


class MonsterDifficultyGuide(View[excel.MonsterDifficultyGuide]):
    ExcelOutput: typing.Final = excel.MonsterDifficultyGuide

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.difficulty_guide_description)

    @property
    def parameter_list(self) -> tuple[float, ...]:
        return tuple(self._excel.parameter_list)


class MonsterGuideConfig(View[excel.MonsterGuideConfig]):
    ExcelOutput: typing.Final = excel.MonsterGuideConfig

    @property
    def id(self) -> int:
        return self._excel.monster_id

    @functools.cached_property
    def __difficulties(self) -> list[MonsterDifficultyGuide]:
        return list(self._game.monster_difficulty_guide(self._excel.difficulty_guide_list))

    def difficulties(self) -> collections.abc.Iterable[MonsterDifficultyGuide]:
        return (MonsterDifficultyGuide(self._game, difficulty._excel) for difficulty in self.__difficulties)

    @functools.cached_property
    def __texts(self) -> list[MonsterTextGuide]:
        return list(self._game.monster_text_guide(self._excel.text_guide_list))

    def texts(self) -> collections.abc.Iterable[MonsterTextGuide]:
        return (MonsterTextGuide(self._game, text._excel) for text in self.__texts)

    @functools.cached_property
    def __tags(self) -> list[MonsterGuideTag]:
        return list(self._game.monster_guide_tag(self._excel.tag_list))

    def tags(self) -> collections.abc.Iterable[MonsterGuideTag]:
        return (MonsterGuideTag(self._game, tag._excel) for tag in self.__tags)

    @functools.cached_property
    def __phases(self) -> list[MonsterGuidePhase]:
        return list(self._game.monster_guide_phase(self._excel.phase_list))

    def phases(self) -> collections.abc.Iterable[MonsterGuidePhase]:
        return (MonsterGuidePhase(self._game, phase._excel) for phase in self.__phases)


class MonsterGuidePhase(View[excel.MonsterGuidePhase]):
    ExcelOutput: typing.Final = excel.MonsterGuidePhase

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.phase_name)

    @functools.cached_property
    def answer(self) -> str:
        return self._game.text(self._excel.phase_answer)

    @functools.cached_property
    def __skills(self) -> list[MonsterGuideSkill]:
        return list(self._game.monster_guide_skill(self._excel.skill_list))

    def skills(self) -> collections.abc.Iterable[MonsterGuideSkill]:
        return (MonsterGuideSkill(self._game, skill._excel) for skill in self.__skills)


class MonsterGuideSkill(View[excel.MonsterGuideSkill]):
    ExcelOutput: typing.Final = excel.MonsterGuideSkill

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.skill_name)

    @functools.cached_property
    def __texts(self) -> list[MonsterGuideSkillText]:
        return list(self._game.monster_guide_skill_text(self._excel.skill_text_id_list))

    def texts(self) -> collections.abc.Iterable[MonsterGuideSkillText]:
        return (MonsterGuideSkillText(self._game, text._excel) for text in self.__texts)


class MonsterGuideSkillText(View[excel.MonsterGuideSkillText]):
    ExcelOutput: typing.Final = excel.MonsterGuideSkillText

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.skill_description)

    @property
    def parameter_list(self) -> tuple[float, ...]:
        return tuple(self._excel.parameter_list)


class MonsterGuideTag(View[excel.MonsterGuideTag]):
    ExcelOutput: typing.Final = excel.MonsterGuideTag

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.tag_name)

    @functools.cached_property
    def brief_description(self) -> str:
        return self._game.text(self._excel.tag_brief_description)

    @functools.cached_property
    def detail_description(self) -> str | None:
        return (
            None if self._excel.tag_detail_description is None else self._game.text(self._excel.tag_detail_description)
        )

    @property
    def parameter_list(self) -> tuple[float, ...]:
        return tuple(self._excel.parameter_list)

    @functools.cached_property
    def __skill(self) -> MonsterSkillConfig | None:
        if self._excel.skill_id is None:
            return None
        skill = self._game.monster_skill_config(self._excel.skill_id)
        assert skill is not None
        return skill

    def skill(self) -> MonsterSkillConfig | None:
        from .monster import MonsterSkillConfig

        return None if self.__skill is None else MonsterSkillConfig(self._game, self.__skill._excel)

    @functools.cached_property
    def __effects(self) -> list[ExtraEffectConfig]:
        return list(self._game.extra_effect_config(self._excel.effect_id))

    def effects(self) -> collections.abc.Iterable[ExtraEffectConfig]:
        from .misc import ExtraEffectConfig

        return (ExtraEffectConfig(self._game, effect._excel) for effect in self.__effects)


class MonsterTextGuide(View[excel.MonsterTextGuide]):
    ExcelOutput: typing.Final = excel.MonsterTextGuide

    @functools.cached_property
    def description(self) -> str:
        return self._game.text(self._excel.text_guide_description)

    @property
    def parameter_list(self) -> tuple[float, ...]:
        return tuple(self._excel.parameter_list)
