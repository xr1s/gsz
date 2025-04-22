import typing

import pydantic

from .base import Model as BaseModel
from .base import get_discriminator
from .task import Model


class SharedFloat(Model):
    key: str


class SharedInt(Model):
    key: str


Value = typing.Annotated[
    typing.Annotated[SharedFloat, pydantic.Tag("SharedFloat")] | typing.Annotated[SharedInt, pydantic.Tag("SharedInt")],
    pydantic.Discriminator(get_discriminator),
]


class ValueSource(BaseModel):
    values: list[Value]
