import typing

import pydantic

from .base import BaseModel, Model, get_discriminator


class SharedFloat(Model):
    key: str
    value: float | None = None


class SharedInt(Model):
    key: str
    value: int | None = None


class SharedString(Model):
    key: str
    value: str | None = None


Value = typing.Annotated[
    typing.Annotated[SharedFloat, pydantic.Tag("SharedFloat")]
    | typing.Annotated[SharedInt, pydantic.Tag("SharedInt")]
    | typing.Annotated[SharedString, pydantic.Tag("SharedString")],
    pydantic.Discriminator(get_discriminator),
]


class ValueSource(BaseModel):
    values: list[Value] | None = None
