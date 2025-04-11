from __future__ import annotations
import functools
import typing

from .. import excel
from .base import View


class AvatarConfig(View[excel.AvatarConfig]):
    ExcelOutput: typing.Final = excel.AvatarConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._excel.avatar_name)
