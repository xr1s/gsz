import typing

import pydantic

from ...excel import Value

ABBR_WORDS = {"3d", "id", "ui", "bgm"}


def alias_generator(field_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in field_name.split("_"))


class BaseModel(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        alias_generator=alias_generator,
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


class Model(BaseModel):
    typ: typing.Annotated[str, pydantic.Field(alias="$type")]


T = typing.TypeVar("T")


class Axis(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0


class FixedValue(BaseModel, typing.Generic[T]):
    is_dynamic: typing.Literal[False] = False
    fixed_value: Value[T]


def get_discriminator(v: typing.Any) -> str:
    if isinstance(v, dict):
        typ = typing.cast(str, v.get("$type"))  # pyright: ignore[reportUnknownMemberType]
        return typ.removeprefix("RPG.GameCore.")
    return v.typ.removeprefix("RPG.GameCore.")


class Custom(BaseModel):
    custom: typing.Literal[True]
    key: str | None = None


class Dynamic(BaseModel):
    class PostfixExpr(BaseModel):
        op_codes: str
        fixed_values: list[Value[float]]
        dynamic_hashes: list[int]

    is_dynamic: typing.Literal[True]
    postfix_expr: PostfixExpr


class Empty(BaseModel):
    pass
