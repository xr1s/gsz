"""末日幻影挑战的提示"""

import typing

import typing_extensions

from .base import ModelID, Text


class MonsterDifficultyGuide(ModelID):
    difficulty_guide_id: int
    difficulty_guide_description: Text
    # [serde(rename = "SkillID")]
    skill_id: int | None = None
    parameter_list: list[float]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.difficulty_guide_id


class MonsterGuideConfig(ModelID):
    monster_id: int
    difficulty: typing.Literal[1, 2, 3, 4]
    difficulty_list: list[typing.Literal[1, 3, 4]]
    tag_list: list[int]
    phase_list: list[int]
    brief_guide: Text | None = None
    difficulty_guide_list: list[int]
    text_guide_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.monster_id


class MonsterGuidePhase(ModelID):
    phase_id: int
    difficulty: typing.Literal[1]
    phase_pic: str
    phase_name: Text
    phase_answer: Text
    phase_description: Text
    skill_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.phase_id


class MonsterGuideSkill(ModelID):
    skill_id: int
    difficulty: typing.Literal[1]
    type: typing.Literal["Normal"]
    skill_name: Text
    skill_text_id_list: list[int]
    skill_answer: Text | None = None

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.skill_id


class MonsterGuideSkillText(ModelID):
    skill_text_id: int
    difficulty: typing.Literal[1]
    skill_description: Text
    parameter_list: list[float]
    effect_id_list: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.skill_text_id


class MonsterGuideTag(ModelID):
    tag_id: int
    tag_name: Text
    tag_brief_description: Text
    tag_detail_description: Text | None = None
    parameter_list: list[float]
    skill_id: int | None = None
    effect_id: list[int]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.tag_id


class MonsterTextGuide(ModelID):
    text_guide_id: int
    text_guide_description: Text
    parameter_list: list[float]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.text_guide_id
