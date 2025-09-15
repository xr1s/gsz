import abc
import enum
import typing

import pydantic
import typing_extensions


class Element(enum.Enum):
    Electric = "Electric"
    """雷"""
    Fire = "Fire"
    """火"""
    Grass = "Grass"
    """草"""
    Ice = "Ice"
    """冰"""
    Rock = "Rock"
    """岩"""
    Water = "Water"
    """水"""
    Wind = "Wind"
    """风"""

    @typing_extensions.override
    def __str__(self) -> str:  # noqa: PLR0911
        match self:
            case Element.Electric:
                return "雷"
            case Element.Fire:
                return "火"
            case Element.Grass:
                return "草"
            case Element.Ice:
                return "冰"
            case Element.Rock:
                return "岩"
            case Element.Water:
                return "水"
            case Element.Wind:
                return "风"


ABBR_WORDS = {"cd"}


def alias_generator(field_name: str) -> str:
    words = field_name.split("_")
    return words[0] + "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in words[1:])


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        alias_generator=alias_generator,
        extra="ignore",
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


Text = int


T = typing.TypeVar("T")


class Value(Model, typing.Generic[T]):
    value: T
