import typing

import pydantic

ABBR_WORDS = {"id", "npc"}


def alias_generator(field_name: str) -> str:
    return "".join(word.upper() if word in ABBR_WORDS else word.capitalize() for word in field_name.split("_"))


class Model(pydantic.BaseModel):
    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(
        alias_generator=alias_generator,
        extra="forbid",
        frozen=True,
        populate_by_name=True,
    )


def get_discriminator(v: typing.Any) -> str:
    if isinstance(v, dict):
        return typing.cast(str, v.get("$type")).removeprefix("RPG.GameCore.")  # pyright: ignore[reportUnknownMemberType]
    return v.typ.removeprefix("RPG.GameCore.")
