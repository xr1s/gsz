import abc
import typing

import pydantic

from . import aliases


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        # extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


class ModelID(abc.ABC, Model):
    @property
    @abc.abstractmethod
    def id(self) -> int: ...


Text = str

T = typing.TypeVar("T")


class ExpFileCfg(Model, typing.Generic[T]):
    exp_filecfg: typing.Annotated[list[T], aliases.EXP_FILE_CONFIG]
