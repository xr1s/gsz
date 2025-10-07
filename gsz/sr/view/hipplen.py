from __future__ import annotations

import functools
import typing

from .. import excel
from .base import View


class ActivityHipplenTrait(View[excel.ActivityHipplenTrait]):
    ExcelOutput: typing.Final = excel.ActivityHipplenTrait

    @functools.cached_property
    def title(self) -> str:
        return self._game.text(self._excel.trait_title)

    @property
    def rarity(self) -> int:
        return self._excel.rarity

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._excel.trait_desc)

    @property
    def desc_param(self) -> tuple[int, ...]:
        return self._excel.trait_desc_param

    @functools.cached_property
    def unlock_desc(self) -> str:
        return self._game.text(self._excel.trait_unlock_desc)

    @property
    def unlock_desc_param(self) -> tuple[int, ...]:
        return self._excel.trait_unlock_desc_param
