import typing

import typing_extensions

from .base import ModelID, Text


class ActivityHipplenTrait(ModelID):
    id_: int
    trait_title: Text
    trait_unlock_desc: Text
    trait_unlock_desc_param: tuple[int, ...]
    trait_desc: Text
    trait_desc_param: tuple[int, ...]
    image_path: str
    effects: tuple[int, ...]
    rarity: typing.Literal[1, 2, 3]

    @property
    @typing_extensions.override
    def id(self) -> int:
        return self.id_
