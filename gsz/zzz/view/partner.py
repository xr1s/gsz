from __future__ import annotations

import functools
import typing

from .. import filecfg
from .base import View


class PartnerConfig(View[filecfg.PartnerConfig]):
    FileCfg: typing.Final = filecfg.PartnerConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._filecfg.name)

    @property
    def icon(self) -> str:
        return self._filecfg.icon
