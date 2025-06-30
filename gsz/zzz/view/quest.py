import functools
import typing

from .. import filecfg
from .base import View


class QuestConfig(View[filecfg.QuestConfig]):
    FileCfg: typing.Final = filecfg.QuestConfig

    @functools.cached_property
    def name(self) -> str:
        return self._game.text(self._filecfg.name)

    @functools.cached_property
    def desc(self) -> str:
        return self._game.text(self._filecfg.desc)

    @functools.cached_property
    def target(self) -> str:
        return self._game.text(self._filecfg.target)

    @functools.cached_property
    def finish_desc(self) -> str:
        return self._game.text(self._filecfg.finish_dec)
