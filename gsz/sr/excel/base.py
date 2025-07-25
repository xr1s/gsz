import abc
import enum
import typing

import pydantic
import pydantic.alias_generators
import typing_extensions


class Element(enum.Enum):
    Fire = "Fire"
    """火"""
    Ice = "Ice"
    """冰"""
    Imaginary = "Imaginary"
    """虚数"""
    Physical = "Physical"
    """物理"""
    Quantum = "Quantum"
    """量子"""
    Thunder = "Thunder"
    """雷"""
    Wind = "Wind"
    """风"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case self.Fire:
                return "火"
            case self.Ice:
                return "冰"
            case self.Imaginary:
                return "虚数"
            case self.Physical:
                return "物理"
            case self.Quantum:
                return "量子"
            case self.Thunder:
                return "雷"
            case self.Wind:
                return "风"


class Path(enum.Enum):
    Knight = "Knight"
    """存护"""
    Mage = "Mage"
    """智识"""
    Memory = "Memory"
    """记忆"""
    Priest = "Priest"
    """丰饶"""
    Rogue = "Rogue"
    """巡猎"""
    Shaman = "Shaman"
    """同谐"""
    Warlock = "Warlock"
    """虚无"""
    Warrior = "Warrior"
    """毁灭"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case self.Knight:
                return "存护"
            case self.Mage:
                return "智识"
            case self.Memory:
                return "记忆"
            case self.Priest:
                return "丰饶"
            case self.Rogue:
                return "巡猎"
            case self.Shaman:
                return "同谐"
            case self.Warlock:
                return "虚无"
            case self.Warrior:
                return "毁灭"


ABBR_WORDS = {"ai", "bg", "bgm", "hp", "id", "npc", "sp", "sfx", "ui"}


def alias_generator(field_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in field_name.split("_"))


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        alias_generator=alias_generator,
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


class ModelID(abc.ABC, Model):
    @property
    @abc.abstractmethod
    def id(self) -> int: ...


class ModelStringID(abc.ABC, Model):
    @property
    @abc.abstractmethod
    def id(self) -> str: ...


class ModelMainSubID(abc.ABC, Model):
    @property
    @abc.abstractmethod
    def main_id(self) -> int: ...

    @property
    @abc.abstractmethod
    def sub_id(self) -> int: ...


class TextHash(Model):
    hash: int


Text = TextHash | str


T = typing.TypeVar("T")


class Value(Model, typing.Generic[T]):
    value: T
